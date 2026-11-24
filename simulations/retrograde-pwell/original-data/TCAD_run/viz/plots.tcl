# ============================================================
# Retrograde P-well TCAD - Sentaurus Visual 그래프 일괄 출력
# 실행:  svisual -bx plots.tcl      (-bx = 그림 저장 가능한 batch 모드)
# 입력:  각 run의 <이름>_BTotal.plx (Sprocess WritePlx, y=0 깊이 프로파일)
# 방법:  <run>_BTotal.plx 로드 -> 총 B 농도 vs 깊이
# 출력:  fig_*.png, 실행 기록 plots_log.txt
# ============================================================
set LOG [open plots_log.txt w]
proc L {msg} { global LOG; puts $LOG $msg; flush $LOG }
proc T {label cmd} {
    if {[catch {uplevel #0 $cmd} r]} { L "ERR  $label : $r"; return "" }
    return $r
}

# 색: 검정/회색 기준 + 구분용 색
set COLORS {#000000 #1f4e9c #c0392b #2e8b57 #e67e22 #7f7f7f #8e44ad #17a2b8 #8b4513}

# run 하나의 깊이 프로파일 로드 (Sprocess WritePlx 결과 <run>_BTotal.plx, y=0 위치 1D)
# 변수 이름: "BTotal x" = 깊이(um), "BTotal y" = 총 B 농도(cm-3)  -- probe로 확인
# (tdr cutline은 x=0 표면점에서 0으로 떨어지는 표시 문제가 있어 plx 사용)
proc cut {run} {
    global CUT
    if {[info exists CUT($run)]} { return $CUT($run) }
    set f ${run}_BTotal.plx
    if {![file exists $f]} { L "MISS $f"; return "" }
    set ds [T "load $run" [list load_file $f -name D_$run]]
    if {$ds eq ""} { return "" }
    set CUT($run) D_$run
    return D_$run
}

# 그래프 1장: name, 제목, {run 라벨 ...}, x범위, y범위
proc fig {name title runs labels {xr {0 2.5}} {yr {1e14 1e18}} {ytype log}} {
    global COLORS
    set P [T "plot $name" [list create_plot -1d -name P_$name]]
    if {$P eq ""} { return }
    set i 0
    foreach run $runs lab $labels {
        set c [cut $run]
        if {$c eq ""} { incr i; continue }
        set cv [T "curve $name/$run" [list create_curve -plot P_$name -dataset $c -axisX "BTotal x" -axisY "BTotal y" -name K_${name}_$i]]
        if {$cv ne ""} {
            T "cprop $name/$run" [list set_curve_prop K_${name}_$i -plot P_$name -label $lab \
                -color [lindex $COLORS [expr {$i % [llength $COLORS]}]] -line_width 3]
        }
        incr i
    }
    # 목표 농도(1e17)와 box 경계(0.5, 1.5 um) 보조선
    T "tgt $name"  [list draw_line -plot P_$name -p1 [list [lindex $xr 0] 1e17] -p2 [list [lindex $xr 1] 1e17]]
    T "b1 $name"   [list draw_line -plot P_$name -p1 [list 0.5 [lindex $yr 0]] -p2 [list 0.5 [lindex $yr 1]]]
    T "b2 $name"   [list draw_line -plot P_$name -p1 [list 1.5 [lindex $yr 0]] -p2 [list 1.5 [lindex $yr 1]]]
    T "ax $name"   [list set_axis_prop -plot P_$name -axis x -title "Depth (um)" -range $xr -title_font_size 16 -label_font_size 14]
    T "ay $name"   [list set_axis_prop -plot P_$name -axis y -title "Total B concentration (cm<sup>-3</sup>)" -type $ytype -range $yr -title_font_size 16 -label_font_size 14]
    T "pp $name"   [list set_plot_prop -plot P_$name -title $title -title_font_size 16 -show_legend]
    T "lg $name"   [list set_legend_prop -plot P_$name -location top_right -label_font_size 13]
    set r [T "export $name" [list export_view fig_$name.png -plots P_$name -format png -resolution 1600x1000 -overwrite]]
    L "DONE fig_$name.png exists=[file exists fig_$name.png]"
}

# ---------------- 그림 목록 ----------------
# 1단계: 단일 에너지 (1e12 cm-2)
set E {200 300 400 500 600 700 800 1000}
set R {}; set B {}
foreach e $E { lappend R S1_E$e; lappend B "$e keV" }
fig 01_stage1_single_energy "Stage 1: single-energy B implant (1e12 cm-2, as-implanted)" $R $B {0 2.5} {1e14 1e17}

# 2단계: 주입 횟수 (총 도즈 1e13 고정, 열처리 없음)
fig 02_stage2_n1to5 "Stage 2: number of implants (total dose 1e13 cm-2, as-implanted)" \
    {S2_n1 S2_n2 S2_n3 S2_n4 S2_n5} {"n=1" "n=2" "n=3" "n=4" "n=5"}

# 3단계 + 4-1: A(매번 RTA) vs B(마지막 1회 RTA) vs C(1회, A와 같은 총 시간)
fig 03_n4_A_B_C "n=4: RTA after every implant (A) vs one final RTA (B, C)" \
    {S2_n4 S3_n4_A S3_n4_B S4a_n4_C} {"as-implanted" "A: RTA x4" "B: RTA x1" "C: RTA x1 (40 s)"}
fig 04_n5_A_B_C "n=5: RTA after every implant (A) vs one final RTA (B, C)" \
    {S2_n5 S3_n5_A S3_n5_B S4a_n5_C} {"as-implanted" "A: RTA x5" "B: RTA x1" "C: RTA x1 (50 s)"}
fig 05_n3_A_B_C "n=3: RTA after every implant (A) vs one final RTA (B, C)" \
    {S2_n3 S3_n3_A S3_n3_B S4a_n3_C} {"as-implanted" "A: RTA x3" "B: RTA x1" "C: RTA x1 (30 s)"}

# box 영역 확대 (선형 축) - A/B/C 차이가 작다는 것을 눈으로 확인
fig 03b_n4_A_B_C_zoom "n=4, box region (linear scale)" \
    {S2_n4 S3_n4_A S3_n4_B S4a_n4_C} {"as-implanted" "A: RTA x4" "B: RTA x1" "C: RTA x1 (40 s)"} {0.4 1.6} {6e16 1.1e17} linear
fig 04b_n5_A_B_C_zoom "n=5, box region (linear scale)" \
    {S2_n5 S3_n5_A S3_n5_B S4a_n5_C} {"as-implanted" "A: RTA x5" "B: RTA x1" "C: RTA x1 (50 s)"} {0.4 1.6} {6e16 1.1e17} linear

# 4-2: Thermal budget (마지막 1회 열처리 조건)
fig 06_n4_budget "n=4: thermal budget of the final anneal" \
    {S3_n4_B S4b_n4_T2 S4b_n4_T3 S4b_n4_T4 S4b_n4_Afurnace} \
    {"RTA 1000C 10s" "T2: 950C 30min" "T3: 1000C 60min" "T4: 1000C 6h" "furnace after every implant"}
fig 07_n5_budget "n=5: thermal budget of the final anneal" \
    {S3_n5_B S4b_n5_T2 S4b_n5_T3 S4b_n5_T4 S4b_n5_Afurnace} \
    {"RTA 1000C 10s" "T2: 950C 30min" "T3: 1000C 60min" "T4: 1000C 6h" "furnace after every implant"}
fig 08_n1_budget "n=1 (400 keV): can a long anneal replace multiple implants?" \
    {S2_n1 S4b_n1_T2 S4b_n1_T3 S4b_n1_T4} \
    {"as-implanted" "T2: 950C 30min" "T3: 1000C 60min" "T4: 1000C 6h"}

# TED on/off
fig 09_n4_TED "n=4: effect of TED (transient enhanced diffusion)" \
    {S3_n4_A S4a_n4_A_TEDoff S3_n4_B S4a_n4_B_TEDoff} \
    {"A, TED on" "A, TED off" "B, TED on" "B, TED off"}

# 검증
fig 10_R1_reproduction "Validation: reproduction of Hsu et al. (2002) sample recipe" \
    {S0_R1repro} {"1500/800/180/100/15 keV + 950C 30min"} {0 3.5} {1e15 1e18}
fig 11_grid_check "Validation: mesh 5 nm vs 2 nm" \
    {S0_grid_5nm S0_grid_2nm} {"5 nm" "2 nm"} {0 2.5} {1e14 1e18}

L "ALL DONE"
close $LOG
exit
