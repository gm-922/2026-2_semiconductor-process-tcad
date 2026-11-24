#header
#endheader
## S4a_n4_C : 4회, 최종 1회 RTA 1000C 40s (A와 열 총량 동일)
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
implant Boron dose= 2.2597E12<cm-2> energy= 700<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 3.0677E12<cm-2> energy= 500<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 2.2235E12<cm-2> energy= 300<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 2.4491E12<cm-2> energy= 200<keV> tilt= 7<degree> rotation= 22<degree>
diffuse temperature= 1000<C> time= 40<s>
SetPlxList { BTotal }
WritePlx S4a_n4_C_BTotal.plx y=0 Silicon
SetPlxList { BActive }
WritePlx S4a_n4_C_BActive.plx y=0 Silicon
struct tdr= S4a_n4_C
