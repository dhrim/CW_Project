# 2026 05 17 0550 reasoning consistency

## 개요
- **데이터:** `benchmark/data/reasoning_sample.jsonl`
- **메타데이터:** `benchmark/data/reasoning_sample.yaml`
- **어댑터:** `models.base_adapter:EchoAdapter`
- **탐지기:** `detectors.reasoning:ReasoningConsistencyDetector`
- **방법/메트릭:** `benchmark/methodology/README.md#2-추론-오류-reasoning-errors` (사용 메트릭: constraint_coverage)

## 실행 커맨드
```bash
cd benchmark
python evaluation/run_benchmark.py data/reasoning_sample.jsonl \
  --adapter models.base_adapter:EchoAdapter \
  --detector detectors.reasoning:ReasoningConsistencyDetector \
  --dataset-meta benchmark/data/reasoning_sample.yaml \
  --methodology benchmark/methodology/README.md#2-추론-오류-reasoning-errors \
  --report ../runs/2026-05-17-0550-reasoning-consistency/report.json
```

## 결과 요약
- 전체 세션: 2
- 플래그된 세션: 1

### 샘플 탐지 레코드
```json
{
  "session_id": "rs-001",
  "is_flagged": false,
  "confidence": 0.0,
  "details": {
    "required": "add_pasta, boil_water, drain",
    "missing": "-"
  },
  "metric": "constraint_coverage"
}
```

## 파일
- `run.log` – 콘솔 출력
- `report.json` – 요약 및 세션별 판정
- `artifacts/responses.jsonl` – 전체 호출/응답 + 탐지 결과
- `README.md` – 본 보고서
