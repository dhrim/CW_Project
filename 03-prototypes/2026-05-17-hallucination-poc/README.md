# 2026-05-17 Hallucination Detection PoC

## 목적
- 4대 오류 중 **환각** 탐지 파이프라인의 최소 실행 예시.
- 모델 어댑터와 탐지기를 분리해 이후 추론 오류·도구 실패·handoff로 확장하기 쉬운 구조를 검증.

## 구성
```
03-prototypes/2026-05-17-hallucination-poc/
├── data/sample_sessions.jsonl
├── detectors/hallucination_detector.py
├── evaluation/run_poc.py
└── models/base_adapter.py
```

## 실행 방법
```bash
cd 03-prototypes/2026-05-17-hallucination-poc
python evaluation/run_poc.py data/sample_sessions.jsonl --threshold 0.6
```

## 확장 포인트
1. **모델 어댑터**
   - `BaseModelAdapter` 인터페이스 구현체를 `models/` 아래에 추가하면 다른 공급자(GPT-4o, Claude, 로컬 Llama 등)로 교체 가능.
   - 어댑터는 `generate(session)`에서 `ModelResponse`를 반환하며, 로그를 `raw` 필드에 보관.
2. **탐지기 레이어**
   - `detectors/` 폴더를 오류 유형별 서브모듈로 확장 가능. 예: `detectors/tool_failure.py`.
   - PoC에서는 토큰 겹침 기반 점수지만, LLM judge, NLI 모델 등으로 교체 가능.
3. **데이터 스키마**
   - 샘플 JSONL은 최소 필드(`session_id`, `reference_facts`, `model_assertions`)만 사용.
   - 상위 벤치마크에서는 동일 구조를 유지하면서 `turns[]`, `tool_calls[]`, `handoff[]` 등 필드를 추가.
4. **리포팅**
   - 현재 CLI 출력만 제공. 추후 `/reports/`에 CSV/JSON 저장 후 상위 평가 파이프라인과 연결.

## 다음 단계 제안
- 이 구조를 참고해 추론 오류/도구 실패/hand-off detector 모듈을 추가.
- 실제 모델 API 연동 어댑터(예: OpenAI) 작성 후 `.env` 기반 설정.
- 벤치마킹 러너(`evaluation/run_benchmark.py`)에서 이 PoC 모듈을 import하도록 통합.
