# -*- coding: utf-8 -*-
"""Retrograde P-Well box profile 분석 스크립트 (노트북에서 실행, Python 3 + numpy/scipy/matplotlib)

결과 .plx 파일을 results/ 폴더에 모은 뒤:
  python analyze.py stage1 results            # 1단계: 에너지별 Rp, dRp, 비대칭도 + 기준점 비교 + 그래프
  python analyze.py design results            # 2단계 설계: 1~4회 에너지·도즈 계산 -> design.json, 예측 분포 pred_n*.txt
  python analyze.py metrics results/S2_n4_BTotal.plx results/S3_n4_B_BTotal.plx ...   # NU, 표면비 등
  python analyze.py compare A.plx B.plx       # 두 결과 차이 (유의차 5% 판정)
  python analyze.py plot A.plx B.plx --out fig.png
  python analyze.py table results             # results 안의 모든 *_BTotal.plx 지표를 표로 (summary.csv)
  python analyze.py diff-length 1000 10s      # 손계산 확산거리 sqrt(2Dt) (L09 확산계수)

판정 기준(진행계획서 4장): NU <= 0.20 합격(<= 0.10 우수), 표면비 <= 0.10, 유의차 >= 5% 또는 NU 차 >= 0.02
"""
import argparse
import itertools
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

TRAPZ = getattr(np, "trapezoid", None) or getattr(np, "trapz")   # numpy 1.x / 2.x 호환

# ---------------- 기준값 ----------------
SUB = 5e15                 # 기판 B (평가 시 차감)
BOX = (0.5, 1.5)           # box 구간 [um]
INNER = (0.6, 1.4)         # 보조 NU 구간
SURF = (0.0, 0.2)          # 표면 저농도 구간
C0 = 1e17                  # 목표 농도
TOTAL = 1e13               # 총 도즈
UNIT_DOSE = 1e12           # 1단계 도즈
NU_PASS, NU_GOOD, SR_PASS, SIG = 0.20, 0.10, 0.10, 0.05
ANCHORS = {200: 0.5, 400: 0.9, 800: 1.6}   # L10 p.26, R1 Fig.4 (그래프 판독)
X = np.round(np.arange(0.0, 4.0 + 1e-9, 0.001), 6)   # 공통 격자 1 nm


# ---------------- 읽기 ----------------
def read_plx(path, field=None):
    """Sentaurus .plx(텍스트)에서 (깊이 um, 농도) 읽기. 블록이 여럿이면 field 이름이 맞는 블록, 없으면 첫 블록."""
    blocks, cur, name = [], [], None
    for line in Path(path).read_text(errors="replace").splitlines():
        m = re.search(r'"([^"]+)"', line)
        nums = re.findall(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", line)
        if m and len(nums) < 2:
            if cur:
                blocks.append((name, cur))
            cur, name = [], m.group(1)
            continue
        try:
            vals = [float(v) for v in re.split(r"[\s,;]+", line.strip()) if v]
        except ValueError:
            continue
        if len(vals) >= 2:
            cur.append((vals[0], vals[1]))
    if cur:
        blocks.append((name, cur))
    if not blocks:
        raise ValueError(f"숫자 데이터 없음: {path}")
    pick = blocks[0][1]
    if field:
        for nm, b in blocks:
            if nm and field.lower() in nm.lower():
                pick = b
                break
    d = np.array(sorted(pick))
    return np.interp(X, d[:, 0], d[:, 1], left=np.nan, right=0.0)


def implanted(c):
    c = np.where(np.isnan(c), 0.0, c)
    return np.clip(c - SUB, 0.0, None)


# ---------------- 지표 ----------------
def nu(c, lo, hi):
    w = (X >= lo) & (X <= hi)
    return (c[w].max() - c[w].min()) / (2 * c[w].mean())


def metrics(c):
    box = (X >= BOX[0]) & (X <= BOX[1])
    surf = (X >= SURF[0]) & (X <= SURF[1])
    avg = c[box].mean()
    total = TRAPZ(c, X) * 1e-4
    return dict(
        NU=nu(c, *BOX), NU_inner=nu(c, *INNER),
        surface_ratio=c[surf].max() / avg,
        box_avg=avg, avg_err=(avg - C0) / C0,
        dose_in_box=TRAPZ(c[box], X[box]) * 1e-4 / total if total > 0 else float("nan"),
        total_dose=total,
    )


def verdict(m):
    nu_v = "우수" if m["NU"] <= NU_GOOD else ("합격" if m["NU"] <= NU_PASS else "불합격")
    sr_v = "합격" if m["surface_ratio"] <= SR_PASS else "불합격"
    return nu_v, sr_v


def moments(c):
    w = c / TRAPZ(c, X)
    rp = TRAPZ(X * w, X)
    sd = math.sqrt(TRAPZ((X - rp) ** 2 * w, X))
    sk = TRAPZ((X - rp) ** 3 * w, X) / sd ** 3
    return rp, sd, sk, X[np.argmax(c)], c.max()


def fmt(m):
    nv, sv = verdict(m)
    return (f"NU={m['NU']:.3f}({nv})  NU_inner={m['NU_inner']:.3f}  표면비={m['surface_ratio']:.3f}({sv})  "
            f"box평균={m['box_avg']:.3g}  평균오차={m['avg_err']*100:+.1f}%  box내도즈={m['dose_in_box']*100:.1f}%")


# ---------------- 명령 ----------------
def stage1_files(folder):
    out = {}
    for p in Path(folder).glob("S1_E*_BTotal.plx"):
        E = int(re.search(r"S1_E(\d+)_", p.name).group(1))
        out[E] = implanted(read_plx(p, "BTotal"))
    if not out:
        sys.exit("S1_E*_BTotal.plx 파일이 없음")
    return dict(sorted(out.items()))


def cmd_stage1(a):
    prof = stage1_files(a.folder)
    rows = ["E_keV,Rp_um,dRp_um,skew,peak_depth_um,peak_cm3,frac_surface,frac_box,anchor_um,anchor_err"]
    print(f"{'E':>6} {'Rp':>7} {'dRp':>7} {'skew':>6} {'peak@':>7} {'표면%':>6} {'box%':>6}  기준점")
    for E, c in prof.items():
        rp, sd, sk, xp, cp = moments(c)
        tot = TRAPZ(c, X)
        fs = TRAPZ(c[X <= SURF[1]], X[X <= SURF[1]]) / tot
        b = (X >= BOX[0]) & (X <= BOX[1])
        fb = TRAPZ(c[b], X[b]) / tot
        anc, err = ANCHORS.get(E), ""
        note = ""
        if anc:
            err = (xp - anc) / anc
            note = f"{anc} um 대비 {err*100:+.0f}% {'OK' if abs(err) <= 0.15 else '⚑ ±15% 벗어남 -> 모델 점검'}"
        print(f"{E:6d} {rp:7.3f} {sd:7.3f} {sk:6.2f} {xp:7.3f} {fs*100:6.1f} {fb*100:6.1f}  {note}")
        rows.append(f"{E},{rp:.4f},{sd:.4f},{sk:.3f},{xp:.4f},{cp:.4g},{fs:.4f},{fb:.4f},{anc or ''},{err if err != '' else ''}")
    Path(a.folder, "stage1_summary.csv").write_text("\n".join(rows), encoding="utf-8")
    plot({f"{E} keV": c for E, c in prof.items()}, Path(a.folder, "stage1_profiles.png"), "1단계: 단일 주입 1e12 (기판 차감)")
    print("-> stage1_summary.csv, stage1_profiles.png 저장")


def optimize_doses(units, energies):
    """주어진 에너지 조합에서 NU 최소 + 표면비<=0.1 이 되도록 도즈 비율 결정 (총 도즈 고정)."""
    from scipy.optimize import minimize, nnls
    box = (X >= BOX[0]) & (X <= BOX[1])
    A = np.array([units[E][box] for E in energies]).T
    q0, _ = nnls(A, np.full(box.sum(), C0))
    if q0.sum() <= 0:
        return None
    q0 = np.maximum(q0, q0.sum() * 0.02)

    def build(lq):
        q = np.exp(lq); q = q / q.sum() * TOTAL
        return q, sum(qi * units[E] for qi, E in zip(q, energies))

    def obj(lq):
        q, c = build(lq)
        m = metrics(c)
        return m["NU"] + 10 * max(0.0, m["surface_ratio"] - SR_PASS)

    r = minimize(obj, np.log(q0), method="Nelder-Mead", options={"maxiter": 400, "xatol": 1e-3, "fatol": 1e-5})
    q, c = build(r.x)
    return q, c, metrics(c)


def quick_score(units, comb):
    """NNLS로 빠른 1차 평가 (총 도즈로 스케일). 반환: (점수, 도즈)"""
    from scipy.optimize import nnls
    box = (X >= BOX[0]) & (X <= BOX[1])
    A = np.array([units[E][box] for E in comb]).T
    q, _ = nnls(A, np.full(box.sum(), C0))
    if q.sum() <= 0:
        return None
    q = q / q.sum() * TOTAL
    c = sum(qi * units[E] for qi, E in zip(q, comb))
    m = metrics(c)
    return m["NU"] + 10 * max(0.0, m["surface_ratio"] - SR_PASS), q


def cmd_design(a):
    prof = stage1_files(a.folder)
    units = {E: c / UNIT_DOSE for E, c in prof.items()}      # 단위 도즈당 분포
    Es = list(units)
    design = {}
    for n in a.n:
        if n == 1:
            cands = []
            for E in Es:
                c = units[E] * TOTAL; m = metrics(c)
                cands.append((m["NU"] + 10 * max(0.0, m["surface_ratio"] - SR_PASS), (E,), np.array([TOTAL]), c, m))
            best = min(cands, key=lambda t: t[0])
        else:
            # 1차: 모든 조합을 NNLS로 빠르게 평가 -> 상위 15개만 정밀 최적화
            quick = []
            for comb in itertools.combinations(Es, n):
                r = quick_score(units, comb)
                if r is not None:
                    quick.append((r[0], comb))
            quick.sort(key=lambda t: t[0])
            best = None
            for _, comb in quick[:15]:
                res = optimize_doses(units, comb)
                if res is None:
                    continue
                q, c, m = res
                score = m["NU"] + 10 * max(0.0, m["surface_ratio"] - SR_PASS)
                if best is None or score < best[0]:
                    best = (score, comb, q, c, m)
        _, comb, q, c, m = best
        order = np.argsort(comb)[::-1]                       # 높은 에너지부터
        Es_sorted = [float(comb[i]) for i in order]
        qs_sorted = [float(q[i]) for i in order]
        design[str(n)] = dict(energies_kev=Es_sorted, doses_cm2=qs_sorted, predicted=m)
        np.savetxt(Path(a.folder, f"pred_n{n}_BTotal.txt"), np.c_[X, c + SUB], header="depth_um conc_cm3 (BTotal 예측, 기판 포함)")
        print(f"n={n}: " + " / ".join(f"{E:g} keV {d:.3g}" for E, d in zip(Es_sorted, qs_sorted)))
        print("      예측 " + fmt(m))
        edge = [E for E in Es_sorted if E in (min(Es), max(Es))]
        if edge:
            print(f"      ⚑ sweep 끝 에너지({edge}) 사용 -> 범위 밖 에너지가 더 나을 수 있음")
    Path(a.folder, "design.json").write_text(json.dumps(design, indent=2, ensure_ascii=False), encoding="utf-8")
    print("-> design.json, pred_n*_BTotal.txt 저장.  다음: python make_decks.py day2 results/design.json")


def load_any(p):
    return implanted(read_plx(p, "BTotal"))


def cmd_metrics(a):
    for p in a.files:
        print(f"{Path(p).name:32s} " + fmt(metrics(load_any(p))))


def cmd_table(a):
    rows = ["run,NU,NU_inner,surface_ratio,box_avg,avg_err,dose_in_box,NU_verdict,SR_verdict"]
    for p in sorted(Path(a.folder).glob("*_BTotal.plx")):
        m = metrics(load_any(p)); nv, sv = verdict(m)
        run = p.name.replace("_BTotal.plx", "")
        rows.append(f"{run},{m['NU']:.4f},{m['NU_inner']:.4f},{m['surface_ratio']:.4f},{m['box_avg']:.4g},{m['avg_err']:.4f},{m['dose_in_box']:.4f},{nv},{sv}")
        print(f"{run:28s} " + fmt(m))
    Path(a.folder, "summary.csv").write_text("\n".join(rows), encoding="utf-8-sig")
    print("-> summary.csv 저장 (엑셀로 열기)")


def cmd_compare(a):
    c1, c2 = load_any(a.a), load_any(a.b)
    box = (X >= BOX[0]) & (X <= BOX[1])
    d = np.abs(c1 - c2)[box] / C0
    i = np.argmax(d)
    m1, m2 = metrics(c1), metrics(c2)
    dnu = m2["NU"] - m1["NU"]
    sig = d[i] >= SIG or abs(dnu) >= 0.02
    print(f"A: {Path(a.a).name}\n   {fmt(m1)}\nB: {Path(a.b).name}\n   {fmt(m2)}")
    print(f"box 안 최대 농도 차이 = 목표의 {d[i]*100:.2f}% (깊이 {X[box][i]:.3f} um), NU 차이 = {dnu:+.3f}")
    print("판정: " + ("유의차 있음 (>= 5% 또는 NU 차 >= 0.02)" if sig else "차이 없음 (< 5%, NU 차 < 0.02)"))


def plot(curves, out, title):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import logging; logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
    import warnings; warnings.filterwarnings("ignore", message="Glyph")
    plt.rcParams["font.family"] = ["Malgun Gothic", "AppleGothic", "NanumGothic", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for lab, c in curves.items():
        ax.semilogy(X, np.maximum(c, 1e13), label=lab, lw=1.4)
    ax.axvspan(*BOX, color="0.9", zorder=0); ax.axvspan(*SURF, color="0.96", zorder=0)
    ax.axhline(C0, color="k", ls="--", lw=0.8)
    ax.set_xlim(0, 2.5); ax.set_ylim(1e14, 1e18)
    ax.set_xlabel("깊이 (µm)"); ax.set_ylabel("주입된 B 농도 (cm$^{-3}$)"); ax.set_title(title)
    ax.legend(fontsize=7, ncol=2); fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


def cmd_plot(a):
    plot({Path(p).name.replace("_BTotal.plx", ""): load_any(p) for p in a.files}, a.out, a.title)
    print(f"-> {a.out}")


def cmd_difflen(a):
    k = 8.617e-5
    T = float(a.T)
    t = a.t.lower()
    sec = float(re.sub(r"[a-z]+", "", t)) * (60 if t.endswith("min") else 3600 if t.endswith("h") else 1)
    D = 10.5 * math.exp(-3.69 / (k * (T + 273.15)))
    print(f"{T:g} C, {sec:g} s : D = {D:.3g} cm2/s, sqrt(2Dt) = {math.sqrt(2*D*sec)*1e7:.1f} nm  (L09: D0=10.5, Ea=3.69 eV)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("stage1"); s.add_argument("folder"); s.set_defaults(f=cmd_stage1)
    s = sp.add_parser("design"); s.add_argument("folder"); s.add_argument("--n", type=int, nargs="+", default=[1, 2, 3, 4]); s.set_defaults(f=cmd_design)
    s = sp.add_parser("metrics"); s.add_argument("files", nargs="+"); s.set_defaults(f=cmd_metrics)
    s = sp.add_parser("table"); s.add_argument("folder"); s.set_defaults(f=cmd_table)
    s = sp.add_parser("compare"); s.add_argument("a"); s.add_argument("b"); s.set_defaults(f=cmd_compare)
    s = sp.add_parser("plot"); s.add_argument("files", nargs="+"); s.add_argument("--out", default="plot.png"); s.add_argument("--title", default=""); s.set_defaults(f=cmd_plot)
    s = sp.add_parser("diff-length"); s.add_argument("T"); s.add_argument("t"); s.set_defaults(f=cmd_difflen)
    a = ap.parse_args(); a.f(a)
