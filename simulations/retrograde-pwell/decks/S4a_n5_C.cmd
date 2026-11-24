#header
#endheader
## S4a_n5_C: 2026-11-24 제출 레시피 기반 선별 정리본
AdvancedCalibration
line x location= 0 spacing= 0.005 tag= top
line x location= 2.5 spacing= 0.005
line x location= 4.0 spacing= 0.02 tag= bottom
line y location= -0.1 spacing= 0.1 tag= left
line y location= 0.1 spacing= 0.1 tag= right
region Silicon xlo= top xhi= bottom ylo= left yhi= right
init concentration= 5E15 field= Boron slice.angle= 180 !DelayFullD
implant Boron dose= 2.0193E+12<cm-2> energy= 750<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 1.6066E+12<cm-2> energy= 600<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 2.7800E+12<cm-2> energy= 450<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 8.7439E+11<cm-2> energy= 300<keV> tilt= 7<degree> rotation= 22<degree>
implant Boron dose= 2.7197E+12<cm-2> energy= 200<keV> tilt= 7<degree> rotation= 22<degree>
diffuse temperature= 1000<C> time= 50<s>
SetPlxList { BTotal }
WritePlx S4a_n5_C_BTotal.plx y=0 Silicon
SetPlxList { BActive }
WritePlx S4a_n5_C_BActive.plx y=0 Silicon
struct tdr= S4a_n5_C
