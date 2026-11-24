# 시뮬레이션 기록 안내

기존 실험 **SIM-000은 내용·입력 데이터·그래프를 그대로 보존**했다. 신규 자료는 별도 연구 묶음으로 관리하며 서로의 격자 결론을 혼동하지 않는다.

| 기록 | 범위 | 데이터 상태 |
|---|---|---|
| [SIM-000](sim-000/README.md) | 20/80/170 keV, 초기 얕은 영역 1·2차 grid 수렴성 | 2026-11-23 실행 자료 보존; **2 nm** 선택, RTA 미검증 |
| [Retrograde P-Well 분석](retrograde-pwell/README.md) | 깊이 0.5~1.5 µm box, 단일 에너지/1~5회 주입/RTA A·B·C/TED/열예산 | 2026-11-24 제공 ZIP의 수치·조건 정리. 파일 전체 원본은 ZIP 참조 |

**중요한 차이:** SIM-000의 2 nm 선택과 신규 자료의 400 keV 2/5 nm 비교에서 5 nm 사용은 서로 다른 구조·에너지·평가 범위에서 나온 판단이다. SIM-000의 내용을 덮어쓰지 않고 병렬 기록한다.

- [새 시뮬레이션 기준과 해석](retrograde-pwell/conditions.md) · [결과](retrograde-pwell/results/README.md) · [선별 입력](retrograde-pwell/decks/README.md)
- 변경 역사: [2026-11-24](../activities/2026-11-24/change-log.md)
- 과거 1~4회 비교 계획은 [2026-11-18 기록](../activities/2026-11-18/simulation-plan-update.md)에 보존.