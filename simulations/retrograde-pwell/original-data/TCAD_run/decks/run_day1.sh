#!/bin/bash
# 서버에서: bash run_day1.sh
# 각 run의 log는 <이름>.log 로 저장됨

echo "== S0_test"; sprocess S0_test.cmd > S0_test.log 2>&1 || echo "!! S0_test 실패 -> S0_test.log 확인"
echo "== S0_grid_5nm"; sprocess S0_grid_5nm.cmd > S0_grid_5nm.log 2>&1 || echo "!! S0_grid_5nm 실패 -> S0_grid_5nm.log 확인"
echo "== S0_grid_2nm"; sprocess S0_grid_2nm.cmd > S0_grid_2nm.log 2>&1 || echo "!! S0_grid_2nm 실패 -> S0_grid_2nm.log 확인"
echo "== S1_E100"; sprocess S1_E100.cmd > S1_E100.log 2>&1 || echo "!! S1_E100 실패 -> S1_E100.log 확인"
echo "== S1_E150"; sprocess S1_E150.cmd > S1_E150.log 2>&1 || echo "!! S1_E150 실패 -> S1_E150.log 확인"
echo "== S1_E200"; sprocess S1_E200.cmd > S1_E200.log 2>&1 || echo "!! S1_E200 실패 -> S1_E200.log 확인"
echo "== S1_E250"; sprocess S1_E250.cmd > S1_E250.log 2>&1 || echo "!! S1_E250 실패 -> S1_E250.log 확인"
echo "== S1_E300"; sprocess S1_E300.cmd > S1_E300.log 2>&1 || echo "!! S1_E300 실패 -> S1_E300.log 확인"
echo "== S1_E350"; sprocess S1_E350.cmd > S1_E350.log 2>&1 || echo "!! S1_E350 실패 -> S1_E350.log 확인"
echo "== S1_E400"; sprocess S1_E400.cmd > S1_E400.log 2>&1 || echo "!! S1_E400 실패 -> S1_E400.log 확인"
echo "== S1_E450"; sprocess S1_E450.cmd > S1_E450.log 2>&1 || echo "!! S1_E450 실패 -> S1_E450.log 확인"
echo "== S1_E500"; sprocess S1_E500.cmd > S1_E500.log 2>&1 || echo "!! S1_E500 실패 -> S1_E500.log 확인"
echo "== S1_E550"; sprocess S1_E550.cmd > S1_E550.log 2>&1 || echo "!! S1_E550 실패 -> S1_E550.log 확인"
echo "== S1_E600"; sprocess S1_E600.cmd > S1_E600.log 2>&1 || echo "!! S1_E600 실패 -> S1_E600.log 확인"
echo "== S1_E650"; sprocess S1_E650.cmd > S1_E650.log 2>&1 || echo "!! S1_E650 실패 -> S1_E650.log 확인"
echo "== S1_E700"; sprocess S1_E700.cmd > S1_E700.log 2>&1 || echo "!! S1_E700 실패 -> S1_E700.log 확인"
echo "== S1_E750"; sprocess S1_E750.cmd > S1_E750.log 2>&1 || echo "!! S1_E750 실패 -> S1_E750.log 확인"
echo "== S1_E800"; sprocess S1_E800.cmd > S1_E800.log 2>&1 || echo "!! S1_E800 실패 -> S1_E800.log 확인"
echo "== S1_E900"; sprocess S1_E900.cmd > S1_E900.log 2>&1 || echo "!! S1_E900 실패 -> S1_E900.log 확인"
echo "== S1_E1000"; sprocess S1_E1000.cmd > S1_E1000.log 2>&1 || echo "!! S1_E1000 실패 -> S1_E1000.log 확인"
