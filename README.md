# CW_Project

벤치마킹 파이프라인을 구축하고 실행 결과를 관리하는 레포지토리입니다. 목표는 에이전트가 겪는 네 가지 핵심 오류(환각, 추론 오류, 도구 사용 실패, handoff 실패)를 빠르게 감지·정량화할 수 있는 구조를 마련하는 것입니다.

## 디렉터리 구조
| 경로 | 설명 |
| --- | --- |
| `benchmark/` | 실행 가능한 스캐폴드. 데이터셋(JSONL+YAML 메타), 모델 어댑터, 탐지기, 범용 러너(`evaluation/run_benchmark.py`)가 포함됩니다. |
| `research/` | 서베이·계획 문서 (`research/surveys`, `research/plans`). 요구사항, 기존 연구, 인프라 계획이 여기에 정리됩니다. |
| `runs/` | 실제 벤치마킹 실행 기록. 현재는 `2026-05-17-0600-echo-bundle/` 아래에 환각/추론/도구/handoff 결과가 묶여 있습니다. 각 하위 폴더에는 `run.log`, `report.json`, `artifacts/responses.jsonl`, `README.md`가 들어 있습니다. |

## 실행 방법 요약
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
- 데이터만 교체하면 추론/도구/handoff 벤치마크도 동일 러너로 실행할 수 있습니다.

## 문서 & 참고
- `benchmark/data/README.md`: 데이터 스키마 및 샘플 데이터셋 목록
- `benchmark/methodology/README.md`: 각 오류 유형별 방법론/메트릭
- `research/plans/01-benchmarking-build-plan.md`: 전체 구축 계획 및 인프라 고려 사항

## 실행 결과 확인
- 최신 번들: `runs/2026-05-17-0600-echo-bundle/`
  - 하위 폴더(`hallucination`, `reasoning`, `tool-failure`, `handoff`)에 세부 보고서가 있으므로, 경영진은 README 표로, 실무자는 `artifacts/responses.jsonl`로 전체 호출을 확인할 수 있습니다.

필요 시 동일 구조로 다른 모델이나 데이터셋을 추가 실행할 수 있으며, 실행 옵션에 따라 폴더명이 자동으로 정해지도록 스크립트를 사용할 수 있습니다.
