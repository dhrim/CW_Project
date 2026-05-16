# Benchmark Scaffold

이 디렉터리는 벤치마킹 파이프라인의 공통 코드/데이터를 담습니다. 현재는 환각(Hallucination) 탐지 단일 모듈만 예시로 포함하며, 동일 구조를 추론 오류·도구 실패·handoff 탐지로 확장할 예정입니다.

## 구조
```
benchmark/
├── data/
├── detectors/
├── evaluation/
└── models/
```

## 실행 예시
```bash
cd benchmark
python evaluation/run_poc.py data/sample_sessions.jsonl --threshold 0.6
```

이 구조는 `02-plans/01-benchmarking-build-plan.md`에 명시된 파이프라인(데이터 → 스크립트 → 모델 → 탐지기 → 평가)을 그대로 따르며, 각 모듈을 독립적으로 교체하거나 확장할 수 있도록 설계되었습니다.
