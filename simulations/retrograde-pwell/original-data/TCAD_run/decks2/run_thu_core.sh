#!/bin/bash
# 서버에서: bash run_thu_core.sh
# 각 run의 log는 <이름>.log 로 저장됨

echo "== S4b_n2_T2"; sprocess S4b_n2_T2.cmd > S4b_n2_T2.log 2>&1 || echo "!! S4b_n2_T2 실패 -> S4b_n2_T2.log 확인"
echo "== S4b_n2_T3"; sprocess S4b_n2_T3.cmd > S4b_n2_T3.log 2>&1 || echo "!! S4b_n2_T3 실패 -> S4b_n2_T3.log 확인"
echo "== S4b_n2_T4"; sprocess S4b_n2_T4.cmd > S4b_n2_T4.log 2>&1 || echo "!! S4b_n2_T4 실패 -> S4b_n2_T4.log 확인"
echo "== S3_n3_A"; sprocess S3_n3_A.cmd > S3_n3_A.log 2>&1 || echo "!! S3_n3_A 실패 -> S3_n3_A.log 확인"
echo "== S3_n3_B"; sprocess S3_n3_B.cmd > S3_n3_B.log 2>&1 || echo "!! S3_n3_B 실패 -> S3_n3_B.log 확인"
echo "== S3_n4_A"; sprocess S3_n4_A.cmd > S3_n4_A.log 2>&1 || echo "!! S3_n4_A 실패 -> S3_n4_A.log 확인"
echo "== S3_n4_B"; sprocess S3_n4_B.cmd > S3_n4_B.log 2>&1 || echo "!! S3_n4_B 실패 -> S3_n4_B.log 확인"
echo "== S4a_n4_C"; sprocess S4a_n4_C.cmd > S4a_n4_C.log 2>&1 || echo "!! S4a_n4_C 실패 -> S4a_n4_C.log 확인"
echo "== S4b_n4_T2"; sprocess S4b_n4_T2.cmd > S4b_n4_T2.log 2>&1 || echo "!! S4b_n4_T2 실패 -> S4b_n4_T2.log 확인"
echo "== S4b_n4_T3"; sprocess S4b_n4_T3.cmd > S4b_n4_T3.log 2>&1 || echo "!! S4b_n4_T3 실패 -> S4b_n4_T3.log 확인"
echo "== S4b_n4_T4"; sprocess S4b_n4_T4.cmd > S4b_n4_T4.log 2>&1 || echo "!! S4b_n4_T4 실패 -> S4b_n4_T4.log 확인"
echo "== S4b_n4_Afurnace"; sprocess S4b_n4_Afurnace.cmd > S4b_n4_Afurnace.log 2>&1 || echo "!! S4b_n4_Afurnace 실패 -> S4b_n4_Afurnace.log 확인"
