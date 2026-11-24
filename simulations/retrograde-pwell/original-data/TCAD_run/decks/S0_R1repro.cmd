#header
#endheader
## S0_R1repro : Hsu et al. 2002 시료 2 재현 (Fig. 4 SIMS와 봉우리 위치 비교). 1500 keV는 테이블 범위 경고 시 Monte Carlo 필요
## 생성: make_decks.py (기준값 = TCAD_프로젝트_진행계획서_v2 3장)
AdvancedCalibration
## TED 포함: AdvancedCalibration 기본 확산 모델 사용

## ---- Mesh (X = 깊이, um) ----
line x location= 0    spacing= 0.005  tag= top
line x location= 2.5  spacing= 0.005
line x location= 4.0  spacing= 0.02  tag= bottom
## y는 점 3개 (사실상 1D)
line y location= -0.1 spacing= 0.1 tag= left
line y location= 0.1  spacing= 0.1 tag= right
region Silicon xlo= top xhi= bottom ylo= left yhi= right

## ---- 기판: p형 (100) Si, B 5E15 cm-3 ----
init concentration= 5E15 field= Boron slice.angle= 180 !DelayFullD
implant Boron dose= 3E13<cm-2> energy= 1500<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 3E13<cm-2> energy= 800<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 1E13<cm-2> energy= 180<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 7E12<cm-2> energy= 100<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 6E12<cm-2> energy= 15<keV> tilt= 7<degree> rotation= 22<degree>
diffuse temperature= 950<C> time= 30<min>   ;# R1: furnace 950C 30min N2
SetPlxList { BTotal }
WritePlx S0_R1repro_BTotal.plx y=0 Silicon
SetPlxList { BActive }
WritePlx S0_R1repro_BActive.plx y=0 Silicon
struct tdr= S0_R1repro
