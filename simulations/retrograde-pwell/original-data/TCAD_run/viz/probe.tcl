# Sentaurus Visual batch 문법 확인용 (결과는 probe_out.txt)
set f [open probe_out.txt w]
proc t {f label cmd} {
    if {[catch {uplevel #0 $cmd} r]} { puts $f "ERR  $label : $r" } else { puts $f "OK   $label : $r" }
    flush $f
}
t $f load_tdr   {set ds [load_file S3_n4_A_fps.tdr -name dsA]}
t $f plot2d     {set p2 [create_plot -dataset dsA]}
t $f cut_y      {set cut [create_cutline -plot $p2 -type y -at 0 -name cutA]}
t $f vars_cut   {list_variables -dataset cutA}
t $f vars_ds    {list_variables -dataset dsA}
t $f load_plx   {set dp [load_file S3_n4_A_BTotal.plx -name plxA]}
t $f vars_plx   {list_variables -dataset plxA}
t $f datasets   {list_datasets}
t $f plot1d     {set p1 [create_plot -1d -name P1]}
t $f curve_plx  {create_curve -plot P1 -dataset plxA -axisX [lindex [list_variables -dataset plxA] 0] -axisY [lindex [list_variables -dataset plxA] 1] -name c1}
t $f ylog       {set_axis_prop -plot P1 -axis y -type log}
t $f export     {export_view probe.png -plots P1 -format png -resolution 1200x800 -overwrite}
close $f
exit
