#header
#endheader
## S3_n4_A: 2026-11-24 제출 레시피 기반 선별 정리본
AdvancedCalibration
line x location= 0 spacing= 0.005 tag= top
line x location= 2.5 spacing= 0.005
line x location= 4.0 spacing= 0.02 tag= bottom
line y location= -0.1 spacing= 0.1 tag= left
line y location= 0.1 spacing= 0.1 tag= right
region Silicon xlo= top xhi= bottom ylo= left yhi= right
init concentration= 5E15 field= Boron slice.angle= 180 !DelayFullD
implant Boron dose= 2.2597E+12<cm-2> energy= 700<keV> tilt= 7<degree> rotation= 22<degree>
diffuse temperature= 1000<C> time= 10<s>
implant Boron dose= 3.0677E+12<cm-2> energy= 500<keV> tilt= 7<degree> rotation= 22<degree>
diffuse temperature= 1000<C> time= 10<s>
implant Boron dose= 2.2235E+12<cm-2> energy= 300<keV> tilt= 7<degree> rotation= 22<degree>
diffuse temperature= 1000<C> time= 10<s>
implant Boron dose= 2.4491E+12<cm-2> energy= 200<keV> tilt= 7<degree> rotation= 22<degree>
diffuse temperature= 1000<C> time= 10<s>
SetPlxList { BTotal }
WritePlx S3_n4_A_BTotal.plx y=0 Silicon
SetPlxList { BActive }
WritePlx S3_n4_A_BActive.plx y=0 Silicon
struct tdr= S3_n4_A
