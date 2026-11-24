#!/bin/bash
F=/user/tools/synopsys/sentaurus/T-2022.03/tcad/T-2022.03/lib/sprocess/TclLib/AdvCal/AdvCal_2022.03.fps
ls -l $F
grep -n -e "DiffModel" -e "ClusterModel" $F | grep -v "^\s*#" | head -20
