# Handoff Benchmark

## 개요
- **데이터:** `benchmark/data/handoff_sample.jsonl`
- **메타데이터:** `benchmark/data/handoff_sample.yaml`
- **어댑터:** `models.base_adapter:EchoAdapter`
- **탐지기:** `detectors.handoff:HandoffIntegrityDetector`
- **방법/메트릭:** `benchmark/methodology/README.md#4-handoff-실패` (사용 메트릭: handoff_slot_coverage)

## 실행 커맨드
```bash
cd benchmark
python evaluation/run_benchmark.py data/handoff_sample.jsonl   --adapter models.base_adapter:EchoAdapter   --detector detectors.handoff:HandoffIntegrityDetector   --dataset-meta benchmark/data/handoff_sample.yaml   --methodology benchmark/methodology/README.md#4-handoff-실패   --report ../runs/2026-05-17-0600-echo-bundle/handoff/report.json
```

## 결과 요약
- 전체 세션: 2
- 플래그된 세션: 1

### 샘플 탐지 레코드
```json
{
  "session_id": "ho-001",
  "is_flagged": false,
  "confidence": 0.0,
  "details": {
    "required": "account_id, issue_summary",
    "delivered": "account_id, issue_summary",
    "missing": "-"
  },
  "metric": "handoff_slot_coverage"
}
```

## 파일
- `run.log` – 콘솔 출력
- `report.json` – 요약 및 세션별 판정
- `artifacts/responses.jsonl` – 전체 호출/응답 + 탐지 결과
- `README.md` – 본 보고서
