# CW_Project

벤치마킹 파이프라인을 구축하고 실행 결과를 관리하는 레포지토리입니다. 목표는 에이전트가 겪는 네 가지 핵심 오류(환각, 추론 오류, 도구 사용 실패, handoff 실패)를 빠르게 감지·정량화할 수 있는 구조를 마련하는 것입니다.

## 디렉터리 구조
| 경로 | 설명 |
| --- | --- |
| `benchmark/` | 실행 가능한 스캐폴드. 데이터셋(JSONL+YAML 메타), 모델 어댑터, 탐지기, 범용 러너(`evaluation/run_benchmark.py`)가 포함됩니다. |
| `research/` | 서베이·계획 문서 (`research/surveys`, `research/plans`). 요구사항, 기존 연구, 인프라 계획이 여기에 정리됩니다. |
| `runs/` | 실제 벤치마킹 실행 기록. 현재는 `2026-05-17-0600-echo-bundle/` 아래에 환각/추론/도구/handoff 결과가 묶여 있습니다. 각 하위 폴더에는 `run.log`, `report.json`, `artifacts/responses.jsonl`, `README.md`가 들어 있습니다. |

## 실행 방법 요약
### CLI 직접 지정
```bash
cd benchmark
python evaluation/run_benchmark.py data/sample_sessions.jsonl \
  --adapter models.base_adapter:EchoAdapter \
  --detector detectors.hallucination:SimpleHallucinationDetector \
  --detector-config '{"threshold": 0.6}' \
  --dataset-meta benchmark/data/metadata.sample.yaml \
  --methodology benchmark/methodology/README.md#1-환각-탐지-hallucination \
  --report ../runs/<폴더>/report.json
```

### 설정 파일로 실행 (권장)
```bash
cd benchmark
python evaluation/run_benchmark.py --config configs/echo_hallucination.json
```
- `benchmark/configs/` 아래 JSON 파일에 dataset/adapter/detector/메타 정보를 선언하면 CLI가 훨씬 짧아집니다.
- 데이터나 탐지기만 교체하면 추론/도구/handoff 벤치마크도 같은 방식으로 실행할 수 있습니다.

## 문서 & 참고
- `benchmark/data/README.md`: 데이터 스키마 및 샘플 데이터셋 목록
- `benchmark/methodology/README.md`: 각 오류 유형별 방법론/메트릭
- `benchmark/configs/echo_hallucination.json`: 설정 파일 샘플
- `research/plans/01-benchmarking-build-plan.md`: 전체 구축 계획 및 인프라 고려 사항

## 실행 결과 확인
- 최신 번들: `runs/2026-05-17-0600-echo-bundle/`
  - 하위 폴더(`hallucination`, `reasoning`, `tool-failure`, `handoff`)마다 `run.log`, `report.json`, `artifacts/responses.jsonl`, `README.md`가 포함되어 있습니다.

필요 시 동일 구조로 다른 모델이나 데이터셋을 추가 실행할 수 있으며, 실행 옵션에 따라 폴더명이 자동으로 정해지도록 스크립트를 사용할 수 있습니다.

## 새 모델/데이터/벤치마크 추가 가이드
- **새 모델 어댑터:** `benchmark/README.md`의 “모델 어댑터 작성 가이드” 절차를 따르고, `benchmark/models/`에 구현 후 설정 파일에서 어댑터 경로만 바꾸면 됩니다.
- **새 데이터셋:** `benchmark/data/README.md`를 참고해 JSONL + YAML 메타파일을 작성하고, `configs/*.json` 또는 CLI에서 `data_path`/`--dataset-meta`를 교체합니다.
- **새 벤치마킹 대상:** `benchmark/methodology/README.md`에 방법론을 정의하고, `benchmark/detectors/`에 대응 탐지기를 추가한 뒤 설정 파일에서 `--detector`를 교체하면 됩니다.
