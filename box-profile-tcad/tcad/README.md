# Sentaurus Process 입력 파일 — 미실행 초안

이 폴더는 `팀공유_box_profile_TCAD.zip`에 있던 Sentaurus Process용 **1D `.cmd` 초안 46개**와 실행 목록 `run_list.csv`, 생성기 `make_decks.py`를 보관합니다.

- **입력 파일 바로 보기:** [decks/](decks/) (예: [3회 주입](decks/S5_3x_asimpl.cmd), [3회 매회 RTA](decks/S6_3x_A_TEDon.cmd), [3회 최종 RTA](decks/S6_3x_B_TEDon.cmd))
- **전체 목록:** [run_list.csv](run_list.csv)에서 실험 ID/단계/목적/파일 경로 확인.
- **코드 생성 방식:** [make_decks.py](make_decks.py)가 `../analysis/designs_lss.json`의 에너지·Dose 후보를 읽어 `decks/`를 생성합니다. 조건 확정 후 별도의 `designs_tcad.json`을 준비해 재생성하도록 설계되어 있습니다.

## 단계 표기
`S0`: 격자 검토 → `S1`: 단일 에너지 주입 → `S1b`: Dose 비례성 → `S2`: 중첩 검증 → `S5`: 1~4회 주입 비교 → `S6`: RTA 시퀀스·모델 비교 → `S6b`: 추가 열예산 실험.

`S3/S4`는 이 패키지에서 독립 명령 파일이 아니라 오프라인 설계 및 분석을 의미합니다. **TCAD 자체의 '시뮬레이션 1·2·3'과 번호가 일치하는 것은 아닙니다.**

## 검증하기 전 실행 완료로 표시하지 마세요
- 소스 코드 주석 `VERIFY`는 설치된 Sentaurus 버전·모델·명령 문법 확인 대상입니다.
- A는 각 이온주입 후 RTA, B는 모든 주입 후 RTA 한 번, C는 **추가 제안**인 누적 열처리 시간 맞춤형 최종 RTA입니다.
- `TEDon`은 `ChargedPair`, `TEDoff`는 `Fermi`로 **다른 확산 모델**을 사용합니다. 이는 TED만 통제한 비교라는 보장이 없습니다.
- `.cmd` 파일 자체는 실행 기록이 아니며, 이 ZIP에는 `.plx`·`.tdr`·로그 출력이 없습니다.
- 팀 공통 프로젝트의 확정 범위는 **주입 1~4회**, **RTA A/B**입니다. C·S6b·on/off는 탐색 후보로 유지합니다.
