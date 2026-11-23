# 이론 계산 / TCAD 결과 후처리 코드

이 디렉터리는 `팀공유_box_profile_TCAD.zip`의 Python 계산 자료를 정리합니다.

| 파일 | 역할 |
|---|---|
| [box_tools.py](box_tools.py) | Gaussian/LSS 단일 프로파일, 주입 조합·Dose 배분 계산, 평탄도/평균 농도, 선형 중첩, RTA 시퀀스 근사 및 TCAD 텍스트 프로파일 로딩 |
| [make_figures.py](make_figures.py) | 사전 예측 그래프 3개 생성 |
| [designs_lss.json](designs_lss.json) | 1~4회 후보 에너지·각 Dose 및 NU 등 **LSS 근사 기반 계산 결과** |

`box_tools.py`는 numpy/scipy에 의존합니다. 학교 서버 TCAD 산출물인 `.plx` 등을 추출한 뒤 오프라인 분석에 활용하도록 작성되었으나 실제 산출물은 ZIP에 없습니다. `designs_lss.json`을 실제 TCAD 결과나 최종 확정 조건으로 오해하지 마세요.
