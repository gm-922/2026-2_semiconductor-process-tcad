#!/bin/bash
# 서버에서: bash run_stage2.sh
# 각 run의 log는 <이름>.log 로 저장됨

echo "== S2_n1"; sprocess S2_n1.cmd > S2_n1.log 2>&1 || echo "!! S2_n1 실패 -> S2_n1.log 확인"
echo "== S2_n2"; sprocess S2_n2.cmd > S2_n2.log 2>&1 || echo "!! S2_n2 실패 -> S2_n2.log 확인"
echo "== S2_n3"; sprocess S2_n3.cmd > S2_n3.log 2>&1 || echo "!! S2_n3 실패 -> S2_n3.log 확인"
echo "== S2_n4"; sprocess S2_n4.cmd > S2_n4.log 2>&1 || echo "!! S2_n4 실패 -> S2_n4.log 확인"
