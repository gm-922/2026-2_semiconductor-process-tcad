#!/bin/bash
# 서버에서: bash run_thu_extra.sh
# 각 run의 log는 <이름>.log 로 저장됨

echo "== S3_n2_A"; sprocess S3_n2_A.cmd > S3_n2_A.log 2>&1 || echo "!! S3_n2_A 실패 -> S3_n2_A.log 확인"
echo "== S3_n2_B"; sprocess S3_n2_B.cmd > S3_n2_B.log 2>&1 || echo "!! S3_n2_B 실패 -> S3_n2_B.log 확인"
echo "== S4a_n2_C"; sprocess S4a_n2_C.cmd > S4a_n2_C.log 2>&1 || echo "!! S4a_n2_C 실패 -> S4a_n2_C.log 확인"
echo "== S4b_n2_Afurnace"; sprocess S4b_n2_Afurnace.cmd > S4b_n2_Afurnace.log 2>&1 || echo "!! S4b_n2_Afurnace 실패 -> S4b_n2_Afurnace.log 확인"
echo "== S4a_n3_C"; sprocess S4a_n3_C.cmd > S4a_n3_C.log 2>&1 || echo "!! S4a_n3_C 실패 -> S4a_n3_C.log 확인"
echo "== S4b_n3_T2"; sprocess S4b_n3_T2.cmd > S4b_n3_T2.log 2>&1 || echo "!! S4b_n3_T2 실패 -> S4b_n3_T2.log 확인"
echo "== S4b_n3_T3"; sprocess S4b_n3_T3.cmd > S4b_n3_T3.log 2>&1 || echo "!! S4b_n3_T3 실패 -> S4b_n3_T3.log 확인"
echo "== S4b_n3_T4"; sprocess S4b_n3_T4.cmd > S4b_n3_T4.log 2>&1 || echo "!! S4b_n3_T4 실패 -> S4b_n3_T4.log 확인"
echo "== S4b_n3_Afurnace"; sprocess S4b_n3_Afurnace.cmd > S4b_n3_Afurnace.log 2>&1 || echo "!! S4b_n3_Afurnace 실패 -> S4b_n3_Afurnace.log 확인"
echo "== S4b_n1_T2"; sprocess S4b_n1_T2.cmd > S4b_n1_T2.log 2>&1 || echo "!! S4b_n1_T2 실패 -> S4b_n1_T2.log 확인"
echo "== S4b_n1_T3"; sprocess S4b_n1_T3.cmd > S4b_n1_T3.log 2>&1 || echo "!! S4b_n1_T3 실패 -> S4b_n1_T3.log 확인"
echo "== S4b_n1_T4"; sprocess S4b_n1_T4.cmd > S4b_n1_T4.log 2>&1 || echo "!! S4b_n1_T4 실패 -> S4b_n1_T4.log 확인"
echo "== S4a_n4_A_TEDoff"; sprocess S4a_n4_A_TEDoff.cmd > S4a_n4_A_TEDoff.log 2>&1 || echo "!! S4a_n4_A_TEDoff 실패 -> S4a_n4_A_TEDoff.log 확인"
echo "== S4a_n4_B_TEDoff"; sprocess S4a_n4_B_TEDoff.cmd > S4a_n4_B_TEDoff.log 2>&1 || echo "!! S4a_n4_B_TEDoff 실패 -> S4a_n4_B_TEDoff.log 확인"
echo "== S4a_n4_C_TEDoff"; sprocess S4a_n4_C_TEDoff.cmd > S4a_n4_C_TEDoff.log 2>&1 || echo "!! S4a_n4_C_TEDoff 실패 -> S4a_n4_C_TEDoff.log 확인"
