# 01. 에이전트 오류 벤치마킹 구축 계획 (Draft)
작성 시각: 2026-05-17 04:55 KST

## 1. 목표 및 범위
- **목표:** 환각, 추론 오류, 도구 사용 실패, handoff 실패를 정량 평가할 수 있는 "새 모델 벤치마킹" 인프라를 48시간 내 POC → 2주 내 MVP 수준까지 확장 가능한 구조로 설계/구축.
- **범위:** 공개/합성 데이터셋 수집, 세션 로그 생성 파이프라인, 모델별 실행/감점 규칙, 리포트 자동화. 모델 자체 개발은 제외하고, 타겟 모델을 갈아 끼울 수 있는 평가 프레임워크 제공.

## 2. 결과물
1. **데이터 자산**
   - 표준 데이터셋 인입(공개) + 자체 합성 템플릿.
   - handoff/조정 실패 라벨을 포함한 JSONL 로그 포맷 정의.
2. **파이프라인**
   - 시나리오 생성 스크립트 (`scripts/`)
   - 탐지기/메트릭 러너 (`detectors/`, `evaluation/`).
   - 타겟 모델 어댑터(`models/{model_id}/adapter.py`).
3. **출력물**
   - 리포트: CSV/Markdown + 시각화 notebook.
   - GitHub README + 예제 실행 명령.
4. **PoC**
   - 최소 1개 모델(OpenAI GPT-4o, Claude Sonnet 등) + 1개 합성 로그로 end-to-end 실행 검증.

## 3. 단계별 계획
| 단계 | 기간(예상) | 주요 작업 | 산출물 |
| --- | --- | --- | --- |
| 0. 셋업 | Day 0 | 리포 구조 정리(01-research, 02-plans, 03-prototypes), 의존성 목록화 | 구조 리포트, requirements 초안 |
| 1. 데이터 수집/정의 | Day 0-1 | HaluEval/SHROOM/ToolBench 등 스키마 통합, handoff synthetic 템플릿 설계 | `/data/{domain}/schema.yaml`, 템플릿 JSON |
| 2. 파이프라인 설계 | Day 1 | 세션 생성(`generate_sessions.py`), 에러 주입 규칙, 로그 스키마 문서화 | `/scripts/README.md`, `/docs/log_schema.md` |
| 3. 탐지기/평가기 | Day 1-2 | 오류 패밀리별 detector 인터페이스, 지표(F1, Error Discovery Rate, KPI 위반율 등) 구현 | `/detectors/*.py`, `/evaluation/run_benchmark.py` |
| 4. 모델 어댑터 계층 | Day 2 | REST/OpenAI, Anthropic, 로컬 모델 호출 모듈 + 공통 trace 수집 | `/models/{provider}/adapter.py` |
| 5. PoC 실행 | Day 2 | samples/manual_sessions.jsonl + GPT-4o adapter로 end-to-end 평가, 리포트 생성 | `/03-prototypes/poc-run-YYYYMMDD/` |
| 6. 문서화 & 배포 | Day 2 | README, runbook, GitHub Actions 초안 | `/README.md`, `/docs/*` |

## 4. 데이터셋 전략
- **기성 데이터:** 01-research/..., 02-survey 참고.
- **부족 영역:** handoff/조정 로그.
  - 합성 전략: LangGraph + OpenTelemetry instrumentation, slot-based context diff, 성공/실패 변형 100세트.
  - 라벨링 기준: `handoff_context_loss`, `handoff_timeout`, `handoff_conflict` 등.
- **저장 포맷:** `session_id`, `turns[]`, `errors[]`, `metrics[]` JSONL.

## 5. 파이프라인 아키텍처 제안
```
benchmark/
├── data/
├── scripts/
│   ├── generate_sessions.py
│   └── inject_errors.py
├── detectors/
│   ├── hallucination.py
│   ├── reasoning.py
│   ├── tool_failure.py
│   └── handoff.py
├── evaluation/
│   └── run_benchmark.py
├── models/
│   ├── openai/
│   ├── anthropic/
│   └── local/
└── reports/
```
- **ETL:** data → scripts (세션 생성) → models (실행) → detectors → evaluation → reports.
- **구성 가능성:** `config/benchmark.yaml`에서 사용할 데이터셋, 모델, 지표를 선언.

## 6. PoC / Prototype 고려 사항
- `03-prototypes/` 하위에 날짜별 폴더 생성 (예: `03-prototypes/2026-05-17-poc-gpt4o/`).
- PoC 구성 요소: 소형 데이터(10 세션), 단일 모델 어댑터, CLI 실행 스크립트.
- CI: GitHub Actions로 lint+smoke test만.

## 7. 리스크 & 대응
| 리스크 | 영향 | 대응 |
| --- | --- | --- |
| 데이터 라이선스 제약 | 공개 배포 제한 | license 필드 명시, 민감 데이터 제거 |
| 모델별 API 변화 | 파이프라인 중단 | adapter 레이어에서 버전 캡슐화, mock adapter 제공 |
| 탐지기 오탐/과탐 | 지표 신뢰도 저하 | human spot-check 샘플, threshold 튜닝 스크립트 |

## 8. 다음 액션
1. 데이터 스키마 문서화 (`docs/log_schema.md`).
2. `scripts/generate_sessions.py` 초기 버전 작성.
3. PoC용 `03-prototypes/2026-05-xx` 디렉터리 생성 및 README 초안.
