#!/bin/bash
# Sentaurus Visual 환경 확인용
R=/user/tools/synopsys/sentaurus/T-2022.03
echo "== svisual:"; which svisual
echo "== tcl examples with create_curve:"
grep -rl --include=*.tcl "create_curve" $R 2>/dev/null | head -8
echo "== manuals:"; ls $R/tcad/current/manuals 2>/dev/null | head; find $R -iname "*visual*ug*" 2>/dev/null | head -5
