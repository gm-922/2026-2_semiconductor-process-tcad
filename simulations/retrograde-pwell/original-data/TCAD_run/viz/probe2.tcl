set f [open probe2_out.txt w]
proc t {f label cmd} {
    if {[catch {uplevel #0 $cmd} r]} { puts $f "ERR  $label : $r" } else { puts $f "OK   $label : $r" }
    flush $f
}
t $f load_plx {load_file S3_n4_A_BTotal.plx -name plxA}
t $f plot1d   {create_plot -1d -name P1}
t $f curve    {create_curve -plot P1 -dataset plxA -axisX "BTotal x" -axisY "BTotal y" -name c1}
t $f ylog     {set_axis_prop -plot P1 -axis y -type log}
t $f e1 {export_view t1.png -plots P1 -format png -overwrite}
t $f e2 {export_view t2.png -plots {P1} -format PNG}
t $f e3 {export_view [file join [pwd] t3.png] -plots P1 -format png -resolution 1200x800 -overwrite}
t $f e4 {export_view t4.png -plots P1}
foreach k {t1 t2 t3 t4} { puts $f "$k exists=[file exists $k.png]" }
close $f
exit
