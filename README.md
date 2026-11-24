# 반도체공정의 이해 | 2026-2 기말프로젝트

Sentaurus Process / Sentaurus Visual을 활용한 4인 공동 연구. 기초 연구 주제는 **다중 에너지 이온주입을 통한 Box-like 도핑 프로파일 형성 및 RTA 공정에 따른 특성 분석**이다.

## 2026-11-24 최신 자료: Retrograde P-Well 지향 설계와 분석

박경록 팀원이 정리해 제공한 **TCAD_run.zip**의 계획·입력 조건·분석 표·결과 그래프 설명을 새 작업 기반으로 정리했다. 표면 저농도와 깊은 영역의 Box-like 고농도를 동시에 추구한다. 실험 대상은 **평판 (100) Si의 깊이 방향 도핑**이며 MOSFET 전기적 특성을 검증하지 않는다. Retrograde P-Well은 실제 공정 동기를 설명하는 맥락이다.

- 기판: p형 Si, B 초기 농도 5×10¹⁵ cm⁻³. 주입: B, tilt 7°, rotation 22°.
- 구간: 표면 **0–0.2 µm** 저농도 / 목표 box **0.5–1.5 µm** / 전이 **0.2–0.5 µm**.
- 목표: box 평균 **1×10¹⁷ cm⁻³** / 초기 주입 총 Dose **1×10¹³ cm⁻²** (주입 횟수 간 동일).
- 판정(팀 자료의 자체 기준): box 비균일도 **NU ≤ 0.20**, 표면비 **≤ 0.10**. NU = (최댓값−최솟값)/(2×평균).
- RTA: **1000 °C, 10 s**. A=매회 RTA, B=최종 1회 RTA. 추가 C=최종 1회, 총 시간 n×10 s.
- 모델: 자료에 기록된 Sentaurus Process T-2022.03 / AdvancedCalibration / 깊이 5 nm. 기판 농도를 뺀 주입 B 농도로 NU와 표면비 평가.
- **변경 범위:** 11/18 기본 구상은 1~4회·A/B까지였다. 11/24 제공 자료에는 **5회 확장 실행, C, TED 및 열예산 비교**가 포함된다. 이는 *제공 자료의 실제 분석 범위*이며, 팀 공식 범위 변경 결재가 이루어졌다고 소급 기록하지 않는다.

### 업로드 자료에 기록된 핵심 결과

| 주입 횟수 | 에너지 조합 (keV) | 주입 직후 NU | 최종 1회 RTA 뒤 NU | 해석 |
|:--:|---|--:|--:|---|
| 1 | 400 | 1.325 | — | 목표 평탄도 미달 |
| 2 | 500 / 200 | 0.705 | 0.685 | 목표 평탄도 미달 |
| 3 | 700 / 500 / 200 | 0.396 | 0.374 | 목표 평탄도 미달 |
| 4 | 700 / 500 / 300 / 200 | 0.215 | 0.207 | NU=0.20 경계 근처 |
| **5 (확장)** | **750 / 600 / 450 / 300 / 200** | **0.183** | **0.166** | **자료의 NU·표면비 기준 통과** |

**주의:** 5회 + 최종 RTA의 box 평균은 약 **8.38×10¹⁶ cm⁻³**로 목표 **1×10¹⁷ cm⁻³**에 미달한다. 따라서 *평탄도·표면비 통과*와 *목표 평균 농도 달성*은 구분한다. 평균 농도를 맞추기 위한 Dose 보정과 공정 산포 검증은 **후속 계획**이다. 총 Dose 보정 후의 4회/5회 실험은 원래의 ‘횟수 간 동일 총 Dose’ 비교와 분리해서 해석해야 한다.

### 연구 기록 바로가기

- [SIM-000: 기존 20/80/170 keV 격자 검증, 원본 보존](simulations/sim-000/README.md)
- [Retrograde P-Well 신규 분석 총괄](simulations/retrograde-pwell/README.md)
- [신규 기준값 및 평가 방법](simulations/retrograde-pwell/conditions.md)
- [신규 결과 표와 해석](simulations/retrograde-pwell/results/README.md)
- [주요 Sentaurus 입력 파일 정리본](simulations/retrograde-pwell/decks/README.md)
- [후속 공정 산포 민감도 검토(미실행)](simulations/retrograde-pwell/next-steps.md)
- [근거 문헌과 검증 범위](simulations/retrograde-pwell/references.md)
- [2026-11-24 박경록 팀원 자료 정리 활동](activities/2026-11-24/박경록.md)
- [변경 이력](activities/2026-11-24/change-log.md) / [전체 활동](activities/README.md) / [시뮬레이션 목록](simulations/README.md) / [기록 템플릿](templates/README.md)

## 자료 상태 및 검증 원칙

제공 ZIP에는 실제 실행 결과로 정리된 **Sprocess .plx·로그 tar**, Sentaurus Visual 그래프 PNG, 설계 JSON, CSV, .cmd, 분석기, 보고서·발표 파일이 포함되어 있다. 이 저장소에는 **조건·결과 수치 요약, 핵심 .cmd 정리본, 분석 규칙 및 출처 목록**을 먼저 게시했다. **용량이 큰 원본 tar/PDF/PPTX/DOCX/PNG 및 모든 원본 .plx 로그는 현재 GitHub에 올리지 않았으며**, 숫자와 그림의 완전한 재현에는 사용자가 제공한 원본 ZIP을 병행 확인해야 한다. 수치·조건은 해당 자료에서 전사했으며 독립적인 TCAD 재실행 또는 문헌 전수 검증을 새로 수행한 것이 아니다.

**구형 box-profile-tcad/는 사용자 요청으로 2026-11-24 저장소 최신 트리에서 삭제**하였다(과거 Git 이력에는 남음). 해당 폴더의 얕은 구간 예비 계산은 현재 연구 결과로 사용하지 않는다.

### 변경 역사

- 2026-11-11: 열산화 주제 선정([과거 회의록](activities/2026-11-11/meeting.md)). 과거 활동은 보존.
- 2026-11-18: 현재 이온주입 연구 주제로 변경([기록](activities/2026-11-18/topic-change.md)).
- 2026-11-23: [SIM-000](simulations/sim-000/README.md)의 1차·2차 격자 검토 기록.
- 2026-11-24: 박경록 팀원 제공 새 목표 구간·측정 수치·확장 시뮬레이션 및 계획 자료 등록.