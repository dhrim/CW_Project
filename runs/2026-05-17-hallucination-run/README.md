# 2026-05-17 Hallucination Benchmark Run

## 개요
- **목적:** 벤치마킹 스캐폴드에 포함된 환각(Hallucination) 탐지 파이프라인이 실제로 결과를 산출하는지 확인
- **데이터:** `benchmark/data/sample_sessions.jsonl` (3개 합성 세션)
- **모델 어댑터:** `EchoAdapter` (샘플용, 모델 API 호출 없음)
- **탐지기:** `SimpleHallucinationDetector` (토큰 겹침 기반)
- **실행 커맨드:**
  ```bash
  cd benchmark
  python3 evaluation/run_benchmark.py data/sample_sessions.jsonl \
    --detector-config '{"threshold": 0.6}' \
    --report ../runs/2026-05-17-hallucination-run/report.json
  ```

## 결과 요약
| 세션 ID | 상태 | 탐지 신뢰도 (1-score) | 비고 |
| --- | --- | --- | --- |
| sess-001 | ✅ 정상 | 0.17 | "프랑스 수도" 질문에 올바른 답(Paris)
| sess-002 | ⚠️ 환각 | 0.62 | Jupiter 대신 Saturn을 반환
| sess-003 | ⚠️ 환각 | 0.50 | 샘플에서는 Iron을 맞게 답해도 토큰 겹침이 낮아 환각으로 분류 (구조 검증 목적)

- **전체 세션 수:** 3
- **탐지된 환각:** 2

### 샘플 호출/응답 (전체는 artifacts 참고)
```json
{
  "session_id": "sess-002",
  "prompt": "Name the largest planet in our solar system.",
  "model_output": "Saturn is the largest planet.",
  "reference_facts": ["Jupiter is the largest planet in the solar system"],
  "detection": {"is_hallucination": true, "confidence": 0.62, "score": "0.38"}
}
```

## 파일
- `run.log` – 원본 CLI 출력
- `artifacts/responses.jsonl` – **모든 세션의 프롬프트/모델 출력/탐지 결과** (대용량 데이터 보관용)
- `README.md` (본 문서) – 경영진/실무자용 요약

> **Note:** 이 실행 결과는 기능 검증용이므로 최종 산출물에는 포함하지 않고 필요 시 삭제 가능합니다.
