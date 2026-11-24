#header
#endheader
## S0_grid_2nm : 격자 2nm: 400 keV 1e12 as-implanted
## 생성: make_decks.py (기준값 = TCAD_프로젝트_진행계획서_v2 3장)
AdvancedCalibration
## TED 포함: AdvancedCalibration 기본 확산 모델 사용

## ---- Mesh (X = 깊이, um) ----
line x location= 0    spacing= 0.002  tag= top
line x location= 2.5  spacing= 0.002
line x location= 4.0  spacing= 0.02  tag= bottom
## y는 점 3개 (사실상 1D)
line y location= -0.1 spacing= 0.1 tag= left
line y location= 0.1  spacing= 0.1 tag= right
region Silicon xlo= top xhi= bottom ylo= left yhi= right

## ---- 기판: p형 (100) Si, B 5E15 cm-3 ----
init concentration= 5E15 field= Boron slice.angle= 180 !DelayFullD
implant Boron dose= 1E12<cm-2> energy= 400<keV> tilt= 7<degree> rotation= 22<degree>
SetPlxList { BTotal }
WritePlx S0_grid_2nm_BTotal.plx y=0 Silicon
SetPlxList { BActive }
WritePlx S0_grid_2nm_BActive.plx y=0 Silicon
struct tdr= S0_grid_2nm
