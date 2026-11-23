"""Figures for the research doc (LSS Gaussian model, pre-TCAD).

python3 make_figures.py  ->  ../figures/fig1_designs.png, ../figures/fig2_anneal_sequences.png
"""
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import box_tools as bt  # noqa: E402

FIG = HERE.parent / "figures"
FIG.mkdir(exist_ok=True)

# palette (dataviz reference instance, light mode)
SURFACE, INK, INK2, MUTED, GRID_C, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, ORANGE = "#2a78d6", "#eb6834"

for f in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",):
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams.update({
    "font.family": ["Noto Sans CJK KR", "Noto Sans CJK JP", "DejaVu Sans"], "font.size": 10,
    "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": GRID_C,
    "grid.linewidth": 0.6, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
})

X = bt.GRID
T = bt.TARGET
design = json.loads((HERE / "designs_lss.json").read_text())


def unit(e):
    rp, s = bt.lss_rp(e)
    return bt.gaussian_profile(rp, s, 1.0)


def box_line(ax):
    ax.plot([0, T["x1"], T["x1"], T["x2"], T["x2"], 0.7], [0, 0, 1, 1, 0, 0],
            color=INK2, lw=1.0, ls=(0, (4, 3)), label="목표 box (1×10¹⁷)")


# ---------------- fig 1: best design per implant count
fig, axes = plt.subplots(2, 2, figsize=(9, 6.2), sharex=True, sharey=True)
for ax, n in zip(axes.flat, ("1", "2", "3", "4")):
    d = design[n]
    parts = [q * unit(e) for e, q in zip(d["energies_kev"], d["doses_cm2"])]
    for p in parts:
        ax.plot(X, p / 1e17, color=MUTED, lw=1.0)
    ax.plot(X, sum(parts) / 1e17, color=BLUE, lw=2.0, label="합성 분포")
    box_line(ax)
    ax.axvspan(T["x1"], T["x2"], color=GRID_C, alpha=0.35, lw=0)
    e_txt = "/".join(f"{e:g}" for e in d["energies_kev"])
    ax.set_title(f"{n}회 주입 ({e_txt} keV) · NU {d['nu']:.2f}", color=INK, fontsize=10.5, loc="left")
    ax.set_xlim(0, 0.7)
    ax.set_ylim(0, 2.6)
for ax in axes[1]:
    ax.set_xlabel("깊이 (µm)")
for ax in axes[:, 0]:
    ax.set_ylabel("B 농도 (×10¹⁷ cm⁻³)")
axes[0, 0].plot([], [], color=MUTED, lw=1.0, label="개별 주입")
axes[0, 0].legend(frameon=False, fontsize=9, loc="upper right", labelcolor=INK2)
fig.suptitle("주입 횟수가 늘수록 목표 구간 안이 평탄해진다 (총 Dose 4×10¹² cm⁻² 고정)",
             x=0.06, ha="left", color=INK, fontsize=12)
fig.text(0.06, 0.005, "Gaussian(LSS, Gibbons 1975) 모델 · Dose 비율은 NU 최소화로 결정 · 열처리 전",
         color=MUTED, fontsize=8.5)
fig.tight_layout(rect=(0, 0.02, 1, 0.96))
fig.savefig(FIG / "fig1_designs.png", dpi=160)

# ---------------- fig 2: anneal-sequence differences, 3x design
d = design["3"]
order = sorted(zip(d["energies_kev"], d["doses_cm2"]), reverse=True)
parts = [q * unit(e) for e, q in order]
qs = [q for _, q in order]
cases = [("1050°C 10 s · 순수 확산", 1050, 10, 0.0),
         ("1050°C 10 s · TED 시나리오 (+50 s 상당)", 1050, 10, 50.0),
         ("1000°C 30 min · 순수 확산", 1000, 1800, 0.0)]
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
for ax, (title, temp, t, ted) in zip(axes, cases):
    r = bt.anneal_sequences(parts, temp, t, doses=qs, ted_s=ted)
    ax.axhline(0, color=AXIS, lw=1.0)
    ax.axvspan(T["x1"], T["x2"], color=GRID_C, alpha=0.35, lw=0)
    ax.plot(X, (r["A_each"] - r["B_final"]) / T["c0"] * 100, color=BLUE, lw=2.0, label="A 매번 RTA − B 최종 1회")
    ax.plot(X, (r["C_final_cumulative"] - r["B_final"]) / T["c0"] * 100, color=ORANGE, lw=2.0,
            label="C 최종 누적시간 − B 최종 1회")
    mx = abs(r["A_each"] - r["B_final"]).max() / T["c0"] * 100
    ax.set_title(f"{title}\nA−B 최대 {mx:.1f}%", color=INK, fontsize=10, loc="left")
    ax.set_xlim(0, 0.7)
    ax.set_xlabel("깊이 (µm)")
axes[0].set_ylabel("B 최종 1회 대비 농도 차 (목표 농도의 %)")
axes[0].legend(frameon=False, fontsize=8.5, loc="lower left", labelcolor=INK2)
fig.suptitle("3회 주입: 1050°C 10 s에서 시퀀스 차이는 순수 확산으로는 ~1%, TED가 있으면 ~10%",
             x=0.05, ha="left", color=INK, fontsize=12)
fig.text(0.05, 0.005, "Fick(D 일정, Plummer 강의노트 값) 예측 · TED는 Plummer Ch.8 노트의 1050°C 지속시간·과포화도에서 잡은 대략적 시나리오 · 회색 띠 = 목표 구간",
         color=MUTED, fontsize=8)
fig.tight_layout(rect=(0, 0.03, 1, 0.93))
fig.savefig(FIG / "fig2_anneal_sequences.png", dpi=160)
# ---------------- fig 0: single-energy profiles (theory slide)
fig, ax = plt.subplots(figsize=(8, 4.2))
energies = [20, 50, 80, 100, 130, 170]
shades = [0.35, 0.47, 0.59, 0.71, 0.85, 1.0]
ax.axvspan(T["x1"], T["x2"], color=GRID_C, alpha=0.35, lw=0)
for e, a in zip(energies, shades):
    rp, s = bt.lss_rp(e)
    c = bt.gaussian_profile(rp, s, 1e12) / 1e17
    ax.plot(X, c, color=BLUE, alpha=a, lw=1.8)
    ax.annotate(f"{e} keV", (rp, c.max()), xytext=(0, 4), textcoords="offset points",
                ha="center", color=INK2, fontsize=8.5)
ax.set_xlim(0, 0.7)
ax.set_ylim(0, 1.6)
ax.set_xlabel("깊이 (µm)")
ax.set_ylabel("B 농도 (×10¹⁷ cm⁻³)\nDose 1×10¹² cm⁻²")
ax.set_title("에너지가 높을수록 깊고 넓고 낮은 봉우리: 하나로는 box를 못 만든다", loc="left", color=INK, fontsize=11.5)
fig.text(0.01, 0.005, "Gaussian(LSS, Gibbons 1975) · 회색 띠 = 목표 구간 0.05–0.45 µm · 170 keV 값은 출처 미확인",
         color=MUTED, fontsize=8.5)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(FIG / "fig0_single_profiles.png", dpi=160)

print("saved", sorted(p.name for p in FIG.glob("*.png")))
