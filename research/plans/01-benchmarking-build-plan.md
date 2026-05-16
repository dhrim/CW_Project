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
| 0. 셋업 | Day 0 | 리포 구조 정리(research, research/plans, runs), 의존성 목록화 | 구조 리포트, requirements 초안 |
| 1. 데이터 수집/정의 | Day 0-1 | HaluEval/SHROOM/ToolBench 등 스키마 통합, handoff synthetic 템플릿 설계 | `/data/{domain}/schema.yaml`, 템플릿 JSON |
| 2. 파이프라인 설계 | Day 1 | 세션 생성(`generate_sessions.py`), 에러 주입 규칙, 로그 스키마 문서화 | `/scripts/README.md`, `/docs/log_schema.md` |
| 3. 탐지기/평가기 | Day 1-2 | 오류 패밀리별 detector 인터페이스, 지표(F1, Error Discovery Rate, KPI 위반율 등) 구현 | `/detectors/*.py`, `/evaluation/run_benchmark.py` |
| 4. 모델 어댑터 계층 | Day 2 | REST/OpenAI, Anthropic, 로컬 모델 호출 모듈 + 공통 trace 수집 | `/models/{provider}/adapter.py` |
| 5. PoC 실행 | Day 2 | samples/manual_sessions.jsonl + GPT-4o adapter로 end-to-end 평가, 리포트 생성 | `/runs/poc-run-YYYYMMDD/` |
| 6. 문서화 & 배포 | Day 2 | README, runbook, GitHub Actions 초안 | `/README.md`, `/docs/*` |

## 4. 데이터셋 전략
- **기성 데이터:** `research/surveys/` 이하 자료 참고.
- **부족 영역:** handoff/조정 로그.
  - 합성 전략: LangGraph + OpenTelemetry instrumentation, slot-based context diff, 성공/실패 변형 100세트.
  - 라벨링 기준: `handoff_context_loss`, `handoff_timeout`, `handoff_conflict` 등.
- **저장 포맷:** `session_id`, `turns[]`, `errors[]`, `metrics[]` JSONL.

### 4.1 데이터 규모 가이드
| 구분 | 48h POC | 2주 MVP | 비고 |
| --- | --- | --- | --- |
| 세션 수 (전체) | 최소 50 세션 (각 오류 유형 10+ 포함) | 500~1,000 세션 (각 오류 유형 균형) | 세션=단일 태스크 수행 로그 |
| 환각 라벨 | 200 claim 수준 | 2,000 claim 수준 | SHROOM/HaluEval 혼합 + 자체 생성 |
| 추론 오류/제약 | 30 KPI 시나리오 | 200 KPI 시나리오 | ODCV-Bench 스타일 Mandated/Incentivized |
| 도구 실패 | 40 ToolBench-style 호출 | 300+ 호출 | ToolEmu/SafeToolBench 샘플 변형 |
| handoff 실패 | 20 synthetic | 150 synthetic + 실사용 익명 로그 | slot loss, timeout, conflict 최소 각 50 |
| 저장 용량 | <200MB (JSONL) | 2~5GB (JSONL + 아티팩트) | 장기 보관은 Parquet 변환 고려 |

- **샘플링 정책:** PoC 단계에서는 Balanced sampling, MVP 이후에는 실제 발생률을 반영한 weighted sampling으로 전환.
- **버전 관리:** `data/releases/v{n}` 태그 + `data/README.md`에 출처/라이선스/생성 스크립트 명시.

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
- `runs/` 하위에 날짜별 폴더 생성 (예: `runs/2026-05-17-poc-gpt4o/`).
- PoC 구성 요소: 소형 데이터(10 세션), 단일 모델 어댑터, CLI 실행 스크립트.
- CI: GitHub Actions로 lint+smoke test만.

## 7. 리스크 & 대응
| 리스크 | 영향 | 대응 |
| --- | --- | --- |
| 데이터 라이선스 제약 | 공개 배포 제한 | license 필드 명시, 민감 데이터 제거 |
| 모델별 API 변화 | 파이프라인 중단 | adapter 레이어에서 버전 캡슐화, mock adapter 제공 |
| 탐지기 오탐/과탐 | 지표 신뢰도 저하 | human spot-check 샘플, threshold 튜닝 스크립트 |

## 8. 인프라 & 운영 고려 사항
- **실행 환경**
  - PoC: 로컬 Mac + Python 3.11, GPU 불필요.
  - MVP: 컨테이너 기반 실행(예: Docker + GitHub Actions self-hosted runner) + GPU/TPU 옵션(로컬 모델 평가 시 필요).
- **저장소/버전 관리**
  - 원본 데이터: Git LFS 또는 S3/객체 저장소(`s3://cw-benchmark-data/v1/`).
  - 결과물: `/reports/`는 Git 관리하되, 대용량 로그는 외부 스토리지 경로만 명시.
  - **용량 계획:** POC 단계 0.2GB, MVP 5GB, 장기(>3개월) 20GB 예상. S3 Standard 기준 월 $0.023/GB → 20GB ≈ $0.46/월.
- **비밀/토큰 관리**
  - `.env.example` 제공, 실제 키는 1Password/Secrets Manager에서 주입.
  - GitHub Actions에서는 OpenAI/Anthropic 키를 `ORG_BENCH_*` prefix로 관리.
- **실험 추적**
  - 최소한 run metadata(JSON) 기록: 모델 버전, 프롬프트, 탐지기 커밋 SHA.
  - 장기적으로 MLflow/W&B 연동 고려.
- **비용/자원**
  - 예상 API 비용: POC < $30, MVP 2주 동안 $300~$500 (LLM 호출량 기준).
  - 컴퓨트: 로컬 CPU 16core + 32GB RAM, 필요 시 클라우드 GPU (A10G) 1대 임대.
- **모니터링/알림**

### 8.1 인프라 사양/비용 추정
| 목적 | 사양 | 시간/주기 | 단가(USD) | 추정 비용 |
| --- | --- | --- | --- | --- |
| PoC 실행 (로컬) | Apple Silicon (M3 Pro 12c CPU, 18c GPU), 32GB RAM | 10시간 | sunk cost | 0 |
| 모델 평가 (클라우드) | NVIDIA A10G 24GB GPU, 8vCPU, 45GB RAM (GCP A2 High-GPU) | 20시간/주 | ~$1.46/시간 | ~$116/월 |
| 대규모 회귀 테스트 | NVIDIA A100 40GB, 12vCPU, 85GB RAM (AWS p4d.24xlarge spot) | 5시간/분기 | ~$3.06/시간(spot) | ~$15/분기 |
| 로그/데이터 저장 | S3 Standard 20GB + Glacier Deep Archive 백업 | 상시 | $0.023/GB + $0.00099/GB | ~$0.50/월 |
| CI 파이프라인 | GitHub Actions Ubuntu runner + 캐시 10GB | 빌드당 10분 | 포함 (Pro 플랜) | 0 |
| 모니터링/알림 | CloudWatch Events + Slack Webhook | 상시 | $1/백만 이벤트 | <$1/월 |

- **GPU 선택 기준:**
  - POC는 API 기반 모델만 호출하므로 GPU 불필요.
  - 로컬/오픈소스 모델 비교가 필요하면 A10G(24GB)로 충분. 대규모 컨텍스트 모델은 A100 40GB 이상 필요.
  - 예산 제한 시 RunPod/AWS Spot 사용 고려.
- **API 비용 산정 근거:** GPT-4o Mini 기준 $0.15/1M input tokens, $0.60/1M output tokens. 세션당 4K 토큰 사용 시 10,000세션 → 약 $30.
  - Claude 3.5 Sonnet($3/1M input, $15/1M output)을 사용할 경우 동일 사용량에서 $180 수준.
- **스토리지 I/O:** JSONL 파일은 저빈도 접근이므로 Standard-Infrequent Access로 전환 시 ~40% 절감. Parquet 변환 시 query 비용 감소.
  - cron 기반 야간 벤치마크 시 Slack/Webhook 알림 구성.
  - 실패 리포트 자동 첨부.

## 9. 다음 액션
1. 데이터 스키마 문서화 (`docs/log_schema.md`).
2. `scripts/generate_sessions.py` 초기 버전 작성.
3. PoC용 `runs/2026-05-xx` 디렉터리 생성 및 README 초안.

## 10. 실제 진행 시 체크포인트
- **거버넌스**: 데이터셋/리포트가 외부 공유 가능한지 보안/법무 승인 절차 명시.
- **QA 프로세스**: 각 릴리즈마다 human review 10% 샘플, 탐지기 로컬 테스트, 회귀 테스트 세트 유지.
- **리소스 예약**: 장시간 벤치마크 시 API rate limit, GPU 예약 스케줄 사전 확보.
- **커뮤니케이션**: 주간/일일 스탠드업 시 진행률 보고(현재 10분 간격 알림 준수). 큰 변경 시 CHANGELOG 업데이트.
- **백업/재현성**: `requirements-lock.txt`, Dockerfile, seed 고정, `make reproduce` 명령으로 동일 결과 재현.
- **PoC → MVP 게이트**: 데이터 규모 충족, 탐지기 정확도(precision>0.7) 및 리포트 자동화 완료 시 다음 단계로 승격.
