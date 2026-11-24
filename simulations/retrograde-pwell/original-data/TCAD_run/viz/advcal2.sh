#!/bin/bash
F=/user/tools/synopsys/sentaurus/T-2022.03/tcad/T-2022.03/lib/sprocess/TclLib/AdvCal/AdvCal_2022.03.fps
sed -n '3215,3226p' $F
sprocess chk_model.cmd > chk_model.log 2>&1
grep CHK chk_model.log
