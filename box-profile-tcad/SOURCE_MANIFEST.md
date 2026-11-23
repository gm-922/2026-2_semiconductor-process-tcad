# ZIP 원본 반영 내역 및 출처 구분

- **원본:** 사용자가 제공한 `팀공유_box_profile_TCAD.zip` (정리일 2026-11-23).
- **원본 파일 총 55개:** 연구 문서 1, `analysis/` Python 2·JSON 1, `figures/` PNG 3, `tcad/` 생성기 Python 1·실행 CSV 1·`.cmd` 46.
- **GitHub 업로드:** 위에서 PNG 3개를 제외한 **원본 코드·텍스트·JSON·CSV 자료 52개**와 신규 설명 README를 반영했습니다. `.cmd` 46개는 `make_decks.py`의 코드 구조와 제공된 계획값으로 생성한 입력 초안입니다.
- **그림:** PNG 원본 3개는 이 저장소에 올리지 않았습니다. 대신 파일의 수식·후보 조건을 활용해 `figures/*.svg` 3개를 **웹 미리보기용으로 재구성**했습니다. 실제 원본 PNG와 그림 품질·세부 렌더링·시뮬레이션 근사 방식에 차이가 있을 수 있습니다. 원본 확인은 ZIP을 보거나 `analysis/make_figures.py`를 실행하세요.
- **추가 설명:** 루트 README의 폴더 안내, `box-profile-tcad/` 및 하위 폴더별 안내 문서, `templates/README.md` 등은 ZIP 원본에 없는 새 문서입니다.
- **실행 여부:** `.cmd`는 **Sentaurus 실행 전 초안**입니다. 원본에 `.plx`, `.tdr`, 실행 로그 또는 실제 TCAD 결과는 없습니다. `VERIFY` 표시 문법·모델은 학교 설치 버전에서 확인해야 합니다.
- **파라미터 지위:** B, 관심 깊이, Dose, RTA 온도/시간, 에너지 배분은 ZIP의 **초기 제안 수치**이며 팀의 공식 확정 조건이 아닙니다. 추가 Case C와 열처리량·모델 비교는 미확정 후보입니다.

기존 `activities/`, `simulations/`의 기록을 소급 수정하거나 이동하지 않습니다.
