#!/bin/bash
R=/user/tools/synopsys/sentaurus/T-2022.03
grep -rh --include='*.tcl' -e 'export_view' -e 'set_axis_prop' -e 'set_curve_prop' -e 'set_legend_prop' -e 'set_plot_prop' $R/tcad/T-2022.03/Applications_Library 2>/dev/null | sed 's/^[ \t]*//' | sort -u | head -60 > ev.txt
cp $R/tcad/T-2022.03/manuals/PDFManual/data/svisual_ug.pdf . 2>/dev/null
svisual -b probe2.tcl >& pv2.log
ls -l *.png ev.txt svisual_ug.pdf
cat probe2_out.txt
