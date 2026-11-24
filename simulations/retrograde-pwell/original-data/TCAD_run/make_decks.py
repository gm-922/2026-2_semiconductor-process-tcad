# -*- coding: utf-8 -*-
"""Sentaurus Process 입력 파일(.cmd) 생성기 — Retrograde P-Well box profile 프로젝트

사용법 (노트북에서, 결과 .cmd 파일을 서버로 올려서 실행):
  python make_decks.py day1                 # 내일: 문법 확인 + 격자 확인 + 1단계(단일 에너지 10개)
  python make_decks.py day2 design.json     # 목요일: 2·3·4단계 (design.json은 analyze.py design 결과)
  python make_decks.py extra                # 여유 있을 때: Hsu(2002) 시료 2 재현, 선형성 확인

문법은 수업 TCAD 과제 입력 파일(과제1·2_sprocess_cmd.txt)과 같은 형식을 따름.
y 방향은 점 3개만 두는 사실상 1D 계산(과제와 같은 2D 문법을 써서 서버 호환성을 확보).
"""
import json
import sys
from pathlib import Path

OUT = Path(__file__).parent / "decks"

# ---------------- 기준값 (진행계획서 3장) ----------------
SUB_B = "5E15"          # p형 기판 B 농도 (R1: 2-5 ohm-cm)
TILT, ROT = 7, 22       # L10 p.30
DX_DEFAULT = 0.005      # 0~2.5 um 격자 간격 [um] (0단계에서 확인)
TOTAL_DOSE = 1e13       # 2단계 총 도즈
RTA = ("1000", "10<s>")                     # T1: 3단계 RTA
BUDGETS = {                                  # 4단계 열예산
    "T2": ("950", "30<min>"),                # R1
    "T3": ("1000", "60<min>"),               # R2
    "T4": ("1000", "360<min>"),              # L09 drive-in 예제
}
S1_ENERGIES = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]   # 50 keV 간격 (설계 해상도)


def header(name, purpose, dx=DX_DEFAULT, ted=True):
    ted_line = ("## TED 포함: AdvancedCalibration 기본 확산 모델 사용" if ted else
                "## TED 제외: 점결함을 풀지 않는 Fermi 모델 (⚑ 서버 매뉴얼에서 모델 이름 확인)\n"
                "pdbSet Silicon Dopant DiffModel Fermi")
    return f"""#header
#endheader
## {name} : {purpose}
## 생성: make_decks.py (기준값 = TCAD_프로젝트_진행계획서_v2 3장)
AdvancedCalibration
{ted_line}

## ---- Mesh (X = 깊이, um) ----
line x location= 0    spacing= {dx}  tag= top
line x location= 2.5  spacing= {dx}
line x location= 4.0  spacing= 0.02  tag= bottom
## y는 점 3개 (사실상 1D)
line y location= -0.1 spacing= 0.1 tag= left
line y location= 0.1  spacing= 0.1 tag= right
region Silicon xlo= top xhi= bottom ylo= left yhi= right

## ---- 기판: p형 (100) Si, B {SUB_B} cm-3 ----
init concentration= {SUB_B} field= Boron slice.angle= 180 !DelayFullD
"""


def sci(x):
    m, e = f"{x:.4e}".split("e")
    return f"{float(m):g}E{int(e)}"


def implant(E, dose):
    return (f"implant Boron dose= {sci(dose)}<cm-2> energy= {E:g}<keV> "
            f"tilt= {TILT}<degree> rotation= {ROT}<degree>\n")


def anneal(T, t, note=""):
    return f"diffuse temperature= {T}<C> time= {t}" + (f"   ;# {note}" if note else "") + "\n"


def write_out(name):
    s = ""
    for f in ("BTotal", "BActive"):
        s += f"SetPlxList {{ {f} }}\nWritePlx {name}_{f}.plx y=0 Silicon\n"
    s += f"struct tdr= {name}\n"
    return s


def save(name, body):
    OUT.mkdir(exist_ok=True)
    with open(OUT / f"{name}.cmd", "w", encoding="utf-8", newline="\n") as f:   # 서버(Linux)용 LF 줄바꿈
        f.write(body)
    return name


# ---------------- day1 ----------------
def day1():
    names = []
    # 문법·단위 확인
    b = header("S0_test", "문법/단위 확인 (400 keV + RTA 10초). 에러 없이 끝나고 log에 10 s로 찍히는지 확인")
    b += implant(400, 1e12) + write_out("S0_test_asimpl") + anneal(*RTA, "10초가 맞게 들어가는지 log 확인") + write_out("S0_test_rta")
    names.append(save("S0_test", b))
    # 격자 확인 (5 nm 기본 vs 2 nm)
    for dx, tag in [(0.005, "5nm"), (0.002, "2nm")]:
        n = f"S0_grid_{tag}"
        names.append(save(n, header(n, f"격자 {tag}: 400 keV 1e12 as-implanted", dx=dx) + implant(400, 1e12) + write_out(n)))
    # 1단계
    for E in S1_ENERGIES:
        n = f"S1_E{E}"
        names.append(save(n, header(n, f"단일 주입 {E} keV, 1e12, 열처리 없음") + implant(E, 1e12) + write_out(n)))
    return names


def extra():
    names = []
    n = "S1_lin400_4e12"
    names.append(save(n, header(n, "선형성: 400 keV 4e12 (1e12 분포 x4 와 비교)") + implant(400, 4e12) + write_out(n)))
    n = "S0_R1repro"
    b = header(n, "Hsu et al. 2002 시료 2 재현 (Fig. 4 SIMS와 봉우리 위치 비교). 1500 keV는 테이블 범위 경고 시 Monte Carlo 필요")
    for E, d in [(1500, 3e13), (800, 3e13), (180, 1e13), (100, 7e12), (15, 6e12)]:
        b += implant(E, d)
    b += anneal("950", "30<min>", "R1: furnace 950C 30min N2") + write_out(n)
    names.append(save(n, b))
    return names


# ---------------- day2 ----------------
def recipe(design, n):
    r = design[str(n)]
    return list(zip(r["energies_kev"], r["doses_cm2"]))   # 높은 에너지부터 정렬되어 있음


def day2(design_path):
    design = json.loads(Path(design_path).read_text(encoding="utf-8"))
    ns = sorted(int(k) for k in design)
    names = []
    for n in ns:
        rec = recipe(design, n)
        desc = " / ".join(f"{E:g} keV {d:.3g}" for E, d in rec)
        # 2단계: as-implanted
        nm = f"S2_n{n}"
        names.append(save(nm, header(nm, f"{n}회 주입, 열처리 없음: {desc}") + "".join(implant(E, d) for E, d in rec) + write_out(nm)))
        if n == 1:
            continue
        # 3단계 A: 주입마다 RTA
        nm = f"S3_n{n}_A"
        b = header(nm, f"{n}회, 주입마다 RTA 1000C 10s: {desc}")
        for E, d in rec:
            b += implant(E, d) + anneal(*RTA)
        names.append(save(nm, b + write_out(nm)))
        # 3단계 B: 최종 1회 RTA
        nm = f"S3_n{n}_B"
        names.append(save(nm, header(nm, f"{n}회, 최종 1회 RTA 1000C 10s: {desc}") + "".join(implant(E, d) for E, d in rec) + anneal(*RTA) + write_out(nm)))
        # 4단계 ①: C = 최종 1회, 시간 n배
        nm = f"S4a_n{n}_C"
        names.append(save(nm, header(nm, f"{n}회, 최종 1회 RTA 1000C {10*n}s (A와 열 총량 동일)") + "".join(implant(E, d) for E, d in rec) + anneal("1000", f"{10*n}<s>") + write_out(nm)))
        # 4단계 ②: 열예산 sweep (최종 1회)
        for key, (T, t) in BUDGETS.items():
            nm = f"S4b_n{n}_{key}"
            names.append(save(nm, header(nm, f"{n}회, 최종 1회 {T}C {t}") + "".join(implant(E, d) for E, d in rec) + anneal(T, t) + write_out(nm)))
        # 4단계 ②: 매번 노 열처리
        nm = f"S4b_n{n}_Afurnace"
        b = header(nm, f"{n}회, 주입마다 950C 30min")
        for E, d in rec:
            b += implant(E, d) + anneal("950", "30<min>")
        names.append(save(nm, b + write_out(nm)))
    # n=1 열예산 sweep (선택)
    if 1 in ns:
        rec = recipe(design, 1)
        for key, (T, t) in BUDGETS.items():
            nm = f"S4b_n1_{key}"
            names.append(save(nm, header(nm, f"1회, {T}C {t}") + implant(*rec[0]) + anneal(T, t) + write_out(nm)))
    # 4단계 ①: TED 제외 (최대 회차)
    n = max(ns)
    rec = recipe(design, n)
    for tag in ("A", "B", "C"):
        nm = f"S4a_n{n}_{tag}_TEDoff"
        b = header(nm, f"{n}회 {tag} 방식, TED 제외 모델", ted=False)
        if tag == "A":
            for E, d in rec:
                b += implant(E, d) + anneal(*RTA)
        else:
            b += "".join(implant(E, d) for E, d in rec)
            b += anneal(*RTA) if tag == "B" else anneal("1000", f"{10*n}<s>")
        names.append(save(nm, b + write_out(nm)))
    return names


def write_runner(names, fname):
    lines = ["#!/bin/bash", "# 서버에서: bash " + fname, "# 각 run의 log는 <이름>.log 로 저장됨", ""]
    for n in names:
        lines.append(f'echo "== {n}"; sprocess {n}.cmd > {n}.log 2>&1 || echo "!! {n} 실패 -> {n}.log 확인"')
    with open(OUT / fname, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "day1"
    if mode == "day1":
        nm = day1(); write_runner(nm, "run_day1.sh")
    elif mode == "extra":
        nm = extra(); write_runner(nm, "run_extra.sh")
    elif mode == "day2":
        nm = day2(sys.argv[2])
        s2 = [x for x in nm if x.startswith("S2_")]
        nmax = max(int(x.split("_n")[1][0]) for x in s2)
        core = [x for x in nm if x in (
            [f"S3_n{nmax}_A", f"S3_n{nmax}_B", f"S3_n{nmax-1}_A", f"S3_n{nmax-1}_B", f"S4a_n{nmax}_C",
             f"S4b_n{nmax}_Afurnace"] + [f"S4b_n{k}_{t}" for k in (2, nmax) for t in BUDGETS])]
        rest = [x for x in nm if x not in s2 and x not in core]
        write_runner(s2, "run_stage2.sh")          # 내일: 2단계
        write_runner(core, "run_thu_core.sh")      # 목요일 필수
        write_runner(rest, "run_thu_extra.sh")     # 목요일 여유 시
        print(f"run_stage2.sh {len(s2)}개 / run_thu_core.sh {len(core)}개 / run_thu_extra.sh {len(rest)}개")
    else:
        sys.exit("mode: day1 | day2 design.json | extra")
    print(f"{len(nm)}개 생성 -> {OUT}")
