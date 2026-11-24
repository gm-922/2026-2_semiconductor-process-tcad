# Sentaurus Process 선별 입력 .cmd 정리본

실제 제공 ZIP에는 TCAD_run/decks/, decks2/, decks3/ 아래에 수십 개의 .cmd와 bash 실행 스크립트가 있다. 이 폴더는 원본에 기록된 조건·순서를 토대로 **대표 run의 .cmd를 GitHub 읽기용으로 재구성**한 것이다. **원본 실행 파일 전체의 바이트 단위 보존본이 아니며, 실주행 시 반드시 ZIP의 원본 파일과 대조**한다.

| 파일 | 목적 |
|---|---|
| S0_grid_2nm.cmd / S0_grid_5nm.cmd | 깊은 B 분포 격자 비교 |
| S1_E200.cmd / S1_E400.cmd / S1_E800.cmd | 단일 에너지 대표점 |
| S2_n1.cmd ~ S2_n5.cmd | 총 dose 동일, 1~5회 as-implanted |
| S3_n4_A.cmd / S3_n4_B.cmd / S3_n5_A.cmd / S3_n5_B.cmd | RTA A/B 비교 |
| S4a_n4_C.cmd / S4a_n5_C.cmd | 최종 1회, n×10s |
| S4a_n4_B_TEDoff.cmd | Fermi 모델 비교 |
| S4b_n4_T2.cmd / T3.cmd / T4.cmd, S4b_n5_T2.cmd / T3.cmd / T4.cmd | 열예산 sweep |

핵심 명령:
- AdvancedCalibration
- line x location=... spacing=... ; region Silicon xlo=top xhi=bottom ylo=left yhi=right
- init concentration=5E15 field=Boron slice.angle=180 !DelayFullD
- implant Boron dose=...<cm-2> energy=...<keV> tilt=7<degree> rotation=22<degree>
- diffuse temperature=...<C> time=...<s> 또는 <min>
- SetPlxList/WritePlx로 BTotal/BActive 출력, struct tdr=...

이 파일의 실행 가능성은 새 서버에서 검증하지 않았다. 서식·온도·시간·주입 순서는 원본과 맞추었으나, 로그·.plx의 원본으로 발표/재현을 검증해야 한다.