#!/bin/bash
rm -f fig_*.png
# 서버 retro_well 폴더에서: bash run_plots.sh
svisual -bx plots.tcl > plots_svisual.log 2>&1
cat plots_log.txt
ls -l fig_*.png
rm -f figs.tar; tar cf figs.tar fig_*.png plots_log.txt plots_svisual.log
