"""Box-profile design and analysis tools for multi-energy boron implants.

Works on any depth profile: Gaussian (LSS) for pre-TCAD estimates, or profiles
exported from TCAD (e.g. Sentaurus WritePlx) once Step 1 runs exist.

Sub-commands (run `python3 box_tools.py -h`):
  metrics      evaluate one profile against the target box
  optimize     choose energies + dose ratios for n = 1..4 implants from unit-dose profiles
  superpose    compare a TCAD multi-implant profile with the sum of single-implant profiles
  anneal       Fick (constant-D) prediction for anneal sequences A / B / C

All depths are in um, concentrations in cm^-3, doses in cm^-2.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.optimize import minimize, nnls

# ---------------------------------------------------------------- constants
K_B = 8.617e-5  # eV/K

# Intrinsic boron diffusivity, D = D0 * exp(-Ea / kT)  [cm^2/s, eV]
# Sources (see the research doc, section 8):
#   plummer: Plummer, Deal & Griffin, Silicon VLSI Technology, Ch. 7 notes
#   jaeger : Jaeger, Introduction to Microelectronic Fabrication, Table 4.1
D_SETS = {"plummer": (1.0, 3.5), "jaeger": (10.5, 3.69)}

# LSS range statistics for B in Si (Gibbons, Johnson & Mylroie 1975).
# 20-150 keV verified against a reproduction of the Gibbons table; 170 keV is unverified.
LSS_B_SI = {20: (0.0662, 0.0283), 30: (0.0987, 0.0371), 40: (0.1302, 0.0443),
            50: (0.1608, 0.0504), 80: (0.2465, 0.0641), 100: (0.2994, 0.0710),
            130: (0.3737, 0.0790), 150: (0.4205, 0.0834), 170: (0.4654, 0.0872)}

# Design target (team decision; see research doc 2-2)
TARGET = dict(x1=0.05, x2=0.45, c0=1e17, inner=(0.10, 0.40))

GRID = np.round(np.arange(0.0, 1.0 + 1e-9, 0.0005), 6)  # 0.5 nm common grid, 0-1 um


def diffusivity(temp_c: float, source: str = "plummer") -> float:
    d0, ea = D_SETS[source]
    return d0 * math.exp(-ea / (K_B * (temp_c + 273.15)))


# ---------------------------------------------------------------- profiles
def gaussian_profile(rp: float, drp: float, dose: float = 1.0, x=GRID) -> np.ndarray:
    """Gaussian implant profile. rp, drp in um; returns cm^-3 for `dose` cm^-2."""
    return dose / (math.sqrt(2 * math.pi) * drp * 1e-4) * np.exp(-(x - rp) ** 2 / (2 * drp ** 2))


def lss_rp(energy_kev: float) -> tuple[float, float]:
    """Log-log interpolation inside the tabulated 20-170 keV range."""
    es = np.array(sorted(LSS_B_SI))
    if not es[0] <= energy_kev <= es[-1]:
        raise ValueError(f"{energy_kev} keV is outside the LSS table (20-170 keV)")
    rp = np.exp(np.interp(math.log(energy_kev), np.log(es), np.log([LSS_B_SI[e][0] for e in es])))
    drp = np.exp(np.interp(math.log(energy_kev), np.log(es), np.log([LSS_B_SI[e][1] for e in es])))
    return float(rp), float(drp)


def load_profile(path: str | Path, x=GRID, column: int = 1) -> np.ndarray:
    """Read a 2+ column text profile (depth_um, conc, ...) such as a Sentaurus .plx.

    Non-numeric lines (headers, field names, braces) are skipped. The profile is
    interpolated onto `x`; outside the data range it is set to 0.
    """
    rows = []
    for line in Path(path).read_text(errors="replace").splitlines():
        parts = re.split(r"[\s,;]+", line.strip())
        try:
            vals = [float(p) for p in parts if p]
        except ValueError:
            continue
        if len(vals) > column:
            rows.append((vals[0], vals[column]))
    if not rows:
        raise ValueError(f"no numeric rows in {path}")
    d = np.array(sorted(rows))
    return np.interp(x, d[:, 0], d[:, 1], left=0.0, right=0.0)


# ---------------------------------------------------------------- metrics
@dataclass
class Metrics:
    nu: float
    nu_inner: float
    c_avg: float
    avg_err: float
    in_window: float
    rmse_rel: float
    deep_edge_um: float
    c_min: float
    c_max: float

    def row(self) -> dict:
        return {k: float(f"{v:.4g}") for k, v in self.__dict__.items()}


def metrics(c: np.ndarray, x=GRID, background: np.ndarray | float = 0.0, t=TARGET) -> Metrics:
    """Evaluate an implanted-boron profile against the box target.

    background: concentration to subtract (e.g. a constant substrate level if the
    profile is NetActive rather than BTotal). For BTotal leave it at 0.
    """
    c = np.asarray(c) - background
    win = (x >= t["x1"]) & (x <= t["x2"])
    inner = (x >= t["inner"][0]) & (x <= t["inner"][1])
    cw = c[win]
    c_avg = cw.mean()
    nu = (cw.max() - cw.min()) / (2 * c_avg)
    nu_in = (c[inner].max() - c[inner].min()) / (2 * c[inner].mean())
    total = np.trapezoid(c, x)
    frac = np.trapezoid(cw, x[win]) / total if total > 0 else float("nan")
    rmse = math.sqrt(np.mean((cw - t["c0"]) ** 2)) / t["c0"]
    # deep-edge sharpness: distance from 90 % to 10 % of the window average, beyond x2's plateau
    deep = x >= t["x1"]
    xs, cs = x[deep], c[deep]
    i90 = np.where(cs >= 0.9 * c_avg)[0]
    edge = float("nan")
    if i90.size:
        start = i90[-1]
        below = np.where(cs[start:] <= 0.1 * c_avg)[0]
        if below.size:
            edge = xs[start + below[0]] - xs[start]
    return Metrics(nu, nu_in, c_avg, abs(c_avg - t["c0"]) / t["c0"], frac, rmse, edge, cw.min(), cw.max())


# ---------------------------------------------------------------- design
@dataclass
class Design:
    energies: tuple
    doses: tuple
    metrics: Metrics
    profile: np.ndarray = field(repr=False)


def _nu_only(c, x, t):
    win = (x >= t["x1"]) & (x <= t["x2"])
    cw = c[win]
    return (cw.max() - cw.min()) / (2 * cw.mean())


def _softmax(z):
    w = np.exp(z - z.max())
    return w / w.sum()


def optimize(unit: dict, n: int, q_total: float, x=GRID, t=TARGET, refine_top: int = 10) -> Design:
    """Best n-implant design from unit-dose profiles {energy: profile per 1 cm^-2}.

    Stage 1: every combination of n energies, dose ratios from an NNLS fit to the box.
    Stage 2: the `refine_top` best combinations (by NU) get Nelder-Mead on the dose
             ratios, minimising NU directly (NNLS minimises squared error, not NU).
    Doses are finally scaled so that sum = q_total (team rule: total dose fixed).
    """
    win = (x >= t["x1"]) & (x <= t["x2"])
    energies = sorted(unit)
    mat = np.stack([unit[e][win] for e in energies], 1)
    idx = {e: i for i, e in enumerate(energies)}
    target = np.full(win.sum(), t["c0"])

    def nu_w(cols, w):
        cw = mat[:, cols] @ w
        return (cw.max() - cw.min()) / (2 * cw.mean())

    cand = []
    for combo in itertools.combinations(energies, n):
        cols = [idx[e] for e in combo]
        q, _ = nnls(mat[:, cols], target)
        if q.sum() <= 0:
            continue
        q = q / q.sum()
        cand.append((nu_w(cols, q), combo, q))
    cand.sort(key=lambda r: r[0])

    best = None
    for nu0, combo, q in cand[: max(1, refine_top)]:
        cols = [idx[e] for e in combo]
        if n > 1:
            res = minimize(lambda z: nu_w(cols, _softmax(z)), np.log(np.maximum(q, 1e-6)),
                           method="Nelder-Mead", options=dict(xatol=1e-5, fatol=1e-7, maxiter=4000))
            if res.fun < nu0:
                q = _softmax(res.x)
        nu = nu_w(cols, q)
        if best is None or nu < best[0]:
            best = (nu, combo, q)
    _, combo, q = best
    doses = q * q_total
    c = sum(d * unit[e] for d, e in zip(doses, combo))
    return Design(tuple(combo), tuple(float(d) for d in doses), metrics(c, x, t=t), c)


# ---------------------------------------------------------------- anneal (Fick, constant D)
def diffuse(c: np.ndarray, two_dt_um2: float, x=GRID) -> np.ndarray:
    """Constant-D diffusion of an arbitrary profile: Gaussian convolution with a
    reflecting (zero-flux) surface at x = 0, implemented with a mirror image."""
    if two_dt_um2 <= 0:
        return c.copy()
    dx = x[1] - x[0]
    s = math.sqrt(two_dt_um2)
    k = np.arange(-int(6 * s / dx) - 1, int(6 * s / dx) + 2) * dx
    ker = np.exp(-k ** 2 / (2 * s ** 2))
    ker /= ker.sum()
    mirrored = np.concatenate([c[:0:-1], c])
    out = np.convolve(mirrored, ker, mode="same")[len(c) - 1:]
    return out


def anneal_sequences(parts: list[np.ndarray], temp_c: float, time_s: float,
                     source: str = "plummer", x=GRID, doses=None, ted_s: float = 0.0) -> dict:
    """parts: per-implant profiles in implant order (first implanted first).

    A: RTA after every implant -> k-th implant sees (n-k+1) anneals
    B: one final RTA            -> every implant sees 1 anneal
    C: one final RTA, n x time  -> every implant sees n anneals' worth

    Optional rough TED term (ted_s > 0): each anneal adds a burst of enhanced
    diffusion to ALL boron present, worth `ted_s` equivalent seconds at the
    intrinsic D when the damage comes from the whole total dose. The burst from
    an anneal scales with the dose implanted since the previous anneal (+1 model:
    excess interstitials ~ dose; Plummer notes: TED time constant ~ dose x Rp,
    the Rp factor is ignored here). This is a scenario, not a calibrated model.
    """
    n = len(parts)
    d = diffusivity(temp_c, source)
    u = 2 * d * time_s * 1e8  # 2Dt per anneal in um^2
    w = np.ones(n) / n if doses is None else np.asarray(doses) / np.sum(doses)
    ted_u = 2 * d * ted_s * 1e8  # TED-equivalent 2Dt for a burst from the total dose
    # A: implant k receives the bursts of anneals k..n, each scaled by that step's dose share
    a_extra = [ted_u * w[k:].sum() for k in range(n)]
    return {
        "as_implanted": sum(parts),
        "A_each": sum(diffuse(p, u * (n - k) + a_extra[k], x) for k, p in enumerate(parts)),
        "B_final": sum(diffuse(p, u + ted_u, x) for p in parts),
        "C_final_cumulative": sum(diffuse(p, u * n + ted_u, x) for p in parts),
    }


# ---------------------------------------------------------------- CLI
def _load_unit(args) -> dict:
    """Unit-dose profiles either from TCAD files or from the LSS Gaussian model."""
    unit = {}
    if args.profiles:
        for f in sorted(Path(args.profiles).glob(args.glob)):
            m = re.search(args.energy_regex, f.name)
            if m:
                unit[float(m.group(1))] = load_profile(f) / args.dose_used
        if not unit:
            raise SystemExit(f"no files matching {args.glob} / {args.energy_regex} in {args.profiles}")
    else:
        for e in range(20, 171, args.step):
            rp, drp = lss_rp(e)
            unit[float(e)] = gaussian_profile(rp, drp, 1.0)
    return unit


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    m = sub.add_parser("metrics", help="metrics of one profile file")
    m.add_argument("file")
    m.add_argument("--background", type=float, default=0.0)

    o = sub.add_parser("optimize", help="best energies + doses for n = 1..4")
    o.add_argument("--profiles", help="folder of single-implant TCAD profiles (omit = LSS Gaussian model)")
    o.add_argument("--glob", default="*.plx")
    o.add_argument("--energy-regex", default=r"(\d+(?:\.\d+)?)keV")
    o.add_argument("--dose-used", type=float, default=1e12, help="dose of the single-implant runs")
    o.add_argument("--q-total", type=float, default=4e12)
    o.add_argument("--step", type=int, default=5, help="LSS model energy step, keV")
    o.add_argument("--max-n", type=int, default=4)
    o.add_argument("--out", default="designs.json")

    s = sub.add_parser("superpose", help="multi-implant TCAD profile vs sum of singles")
    s.add_argument("multi")
    s.add_argument("--single", nargs="+", required=True, help="file:dose pairs, e.g. B_40keV.plx:1e12")
    s.add_argument("--doses", nargs="+", type=float, required=True, help="doses used in the multi run")

    a = sub.add_parser("anneal", help="Fick prediction of sequences A/B/C for a design")
    a.add_argument("--design", default="designs.json")
    a.add_argument("--n", type=int, required=True)
    a.add_argument("--temp", type=float, default=1050)
    a.add_argument("--time", type=float, default=10)
    a.add_argument("--d-source", choices=D_SETS, default="plummer")
    a.add_argument("--ted-s", type=float, default=0.0,
                   help="rough TED burst, intrinsic-D equivalent seconds for the total dose (0 = off)")
    a.add_argument("--profiles", help="same as optimize; omit = LSS model")
    a.add_argument("--glob", default="*.plx")
    a.add_argument("--energy-regex", default=r"(\d+(?:\.\d+)?)keV")
    a.add_argument("--dose-used", type=float, default=1e12)
    a.add_argument("--step", type=int, default=5)

    args = ap.parse_args()

    if args.cmd == "metrics":
        print(json.dumps(metrics(load_profile(args.file), background=args.background).row(), indent=2))

    elif args.cmd == "optimize":
        unit = _load_unit(args)
        out = {}
        for n in range(1, args.max_n + 1):
            d = optimize(unit, n, args.q_total)
            out[n] = dict(energies_kev=d.energies, doses_cm2=d.doses, **d.metrics.row())
            print(f"{n}x  E={'/'.join(f'{e:g}' for e in d.energies)} keV  "
                  f"Q={'/'.join(f'{q:.3g}' for q in d.doses)}  NU={d.metrics.nu:.3f}  "
                  f"NU_inner={d.metrics.nu_inner:.3f}  Cavg={d.metrics.c_avg:.3g}  in-window={d.metrics.in_window:.0%}")
        Path(args.out).write_text(json.dumps(out, indent=2))
        print(f"saved {args.out}")

    elif args.cmd == "superpose":
        multi = load_profile(args.multi)
        summed = np.zeros_like(GRID)
        for spec, q in zip(args.single, args.doses):
            f, q_used = spec.rsplit(":", 1)
            summed += load_profile(f) / float(q_used) * q
        win = (GRID >= TARGET["x1"]) & (GRID <= TARGET["x2"])
        dev = np.abs(multi[win] - summed[win]) / summed[win].mean()
        print(f"max |multi - sum| / mean(sum) in window = {dev.max():.2%}  (mean {dev.mean():.2%})")

    elif args.cmd == "anneal":
        design = json.loads(Path(args.design).read_text())[str(args.n)]
        unit = _load_unit(args)
        order = sorted(zip(design["energies_kev"], design["doses_cm2"]), reverse=True)  # high energy first
        parts = [unit[float(e)] * q for e, q in order]
        res = anneal_sequences(parts, args.temp, args.time, args.d_source,
                               doses=[q for _, q in order], ted_s=args.ted_s)
        for k, c in res.items():
            r = metrics(c).row()
            print(f"{k:20s} NU={r['nu']:.3f}  NU_inner={r['nu_inner']:.3f}  Cavg={r['c_avg']:.3g}  deep_edge={r['deep_edge_um']:.3f} um")
        diff = np.abs(res["A_each"] - res["B_final"]).max() / TARGET["c0"]
        print(f"max |A - B| / target = {diff:.2%}")


if __name__ == "__main__":
    main()
