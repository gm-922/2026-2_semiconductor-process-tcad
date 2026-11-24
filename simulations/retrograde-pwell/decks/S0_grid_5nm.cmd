#header
#endheader
## S0_grid_5nm: 2026-11-24 제출 레시피 기반 선별 정리본
AdvancedCalibration
line x location= 0 spacing= 0.005 tag= top
line x location= 2.5 spacing= 0.005
line x location= 4.0 spacing= 0.02 tag= bottom
line y location= -0.1 spacing= 0.1 tag= left
line y location= 0.1 spacing= 0.1 tag= right
region Silicon xlo= top xhi= bottom ylo= left yhi= right
init concentration= 5E15 field= Boron slice.angle= 180 !DelayFullD
implant Boron dose= 1.0000E+12<cm-2> energy= 400<keV> tilt= 7<degree> rotation= 22<degree>
SetPlxList { BTotal }
WritePlx S0_grid_5nm_BTotal.plx y=0 Silicon
SetPlxList { BActive }
WritePlx S0_grid_5nm_BActive.plx y=0 Silicon
struct tdr= S0_grid_5nm
