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

## 모델 어댑터 작성 가이드
1. `benchmark/models/`에 새 파일을 만들고 `BaseModelAdapter`를 상속합니다.
2. `generate(self, session: Dict[str, Any]) -> ModelResponse` 메서드에서 타겟 모델 호출 로직을 구현합니다.
   - 예: OpenAI GPT-4o를 호출하는 경우 `openai.ChatCompletion.create(...)` 후 응답 텍스트를 `ModelResponse.output`에 넣습니다.
   - `raw` 필드에는 latency, tokens, request id 등 추후 분석용 메타데이터를 담습니다.
3. 평가 스크립트에서 원하는 어댑터를 import해 인스턴스화하면 됩니다.
   ```python
   from models.openai_adapter import OpenAIAdapter
   adapter = OpenAIAdapter(model="gpt-4o", api_key=os.environ["OPENAI_API_KEY"])
   ```
4. 공통 환경변수는 `.env.example`에 추가하고, 실제 키는 1Password/Secrets Manager 등 외부 비밀 저장소에서 주입합니다.

## 감지기 확장
- `benchmark/detectors/`에 오류 유형별 모듈을 추가합니다. (예: `reasoning.py`, `tool_failure.py`, `handoff.py`).
- 각 모듈은 공통 `DetectionResult` 데이터클래스를 사용해 일관된 인터페이스를 유지합니다.

이 구조는 `research/plans/01-benchmarking-build-plan.md`에 명시된 파이프라인(데이터 → 스크립트 → 모델 → 탐지기 → 평가)을 그대로 따르며, 각 모듈을 독립적으로 교체하거나 확장할 수 있도록 설계되었습니다.
