#!/bin/bash
# 서버에서: bash run_extra.sh
# 각 run의 log는 <이름>.log 로 저장됨

echo "== S1_lin400_4e12"; sprocess S1_lin400_4e12.cmd > S1_lin400_4e12.log 2>&1 || echo "!! S1_lin400_4e12 실패 -> S1_lin400_4e12.log 확인"
echo "== S0_R1repro"; sprocess S0_R1repro.cmd > S0_R1repro.log 2>&1 || echo "!! S0_R1repro 실패 -> S0_R1repro.log 확인"
