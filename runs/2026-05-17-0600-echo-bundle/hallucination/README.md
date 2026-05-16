# Hallucination Benchmark

## 개요
- **데이터:** `benchmark/data/sample_sessions.jsonl`
- **메타데이터:** `benchmark/data/metadata.sample.yaml`
- **어댑터:** `models.base_adapter:EchoAdapter`
- **탐지기:** `detectors.hallucination:SimpleHallucinationDetector`
- **방법/메트릭:** `benchmark/methodology/README.md#1-환각-탐지-hallucination` (사용 메트릭: token_overlap)

## 실행 커맨드
```bash
cd benchmark
python evaluation/run_benchmark.py data/sample_sessions.jsonl   --adapter models.base_adapter:EchoAdapter   --detector detectors.hallucination:SimpleHallucinationDetector   --dataset-meta benchmark/data/metadata.sample.yaml   --methodology benchmark/methodology/README.md#1-환각-탐지-hallucination   --report ../runs/2026-05-17-0600-echo-bundle/hallucination/report.json
```

## 결과 요약
- 전체 세션: 3
- 플래그된 세션: 2

### 샘플 탐지 레코드
```json
{
  "session_id": "sess-001",
  "is_flagged": false,
  "confidence": 0.16666666666666663,
  "details": {
    "score": "0.83"
  },
  "metric": "token_overlap"
}
```

## 파일
- `run.log` – 콘솔 출력
- `report.json` – 요약 및 세션별 판정
- `artifacts/responses.jsonl` – 전체 호출/응답 + 탐지 결과
- `README.md` – 본 보고서
