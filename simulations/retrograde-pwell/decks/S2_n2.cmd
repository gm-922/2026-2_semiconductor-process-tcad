#header
#endheader
## S2_n2: 2026-11-24 제출 레시피 기반 선별 정리본
AdvancedCalibration
line x location= 0 spacing= 0.005 tag= top
line x location= 2.5 spacing= 0.005
line x location= 4.0 spacing= 0.02 tag= bottom
line y location= -0.1 spacing= 0.1 tag= left
line y location= 0.1 spacing= 0.1 tag= right
region Silicon xlo= top xhi= bottom ylo= left yhi= right
init concentration= 5E15 field= Boron slice.angle= 180 !DelayFullD
implant Boron dose= 5.5692E+12<cm-2> energy= 500<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 4.4308E+12<cm-2> energy= 200<keV> tilt= 7<degree> rotation= 22<degree>
SetPlxList { BTotal }
WritePlx S2_n2_BTotal.plx y=0 Silicon
SetPlxList { BActive }
WritePlx S2_n2_BActive.plx y=0 Silicon
struct tdr= S2_n2
