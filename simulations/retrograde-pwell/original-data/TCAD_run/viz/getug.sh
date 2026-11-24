#!/bin/bash
D=/user/tools/synopsys/sentaurus/T-2022.03/tcad/T-2022.03/manuals/PDFManual/data
ls $D | grep -i -e sproc -e process
cp $D/sprocess_ug.pdf . 2>/dev/null
rm -f ug2.tar; tar cf ug2.tar sprocess_ug.pdf
ls -l ug2.tar
