# Data Onboarding Guide

## JSONL 스키마 (최소)
각 라인은 아래 필드를 포함합니다.

```json
{
  "session_id": "unique-identifier",
  "prompt": "user or system prompt",
  "reference_facts": ["ground truth sentence", "..."],
  "model_assertions": ["example model output"],
  "metadata": {"source": "synthetic"}
}
```

### 필수 필드
- `session_id`: 문자열, 전체 파일에서 유일해야 함.
- `prompt`: 모델 입력.
- `reference_facts`: 탐지기가 비교할 수 있는 정답/근거 리스트. 오류 유형에 따라 `constraints`, `tool_calls`, `handoff` 등 추가 필드를 붙일 수 있음.

### 선택 필드 예시
- `turns`: 멀티턴 대화 로그 배열.
- `tool_calls`: 에이전트→도구 호출 히스토리.
- `handoff`: 에이전트 간 컨텍스트 전달 정보.

## 데이터셋 추가 절차
1. `benchmark/data/<dataset-name>.jsonl` 파일 생성 후 위 스키마로 입력.
2. (선택) `benchmark/data/<dataset-name>.yaml`에 메타데이터(출처, 라이선스, 태그)를 기록.
3. 추후 실행 시 `python evaluation/run_benchmark.py benchmark/data/<dataset-name>.jsonl ...` 형태로 지정.
4. 대규모 데이터는 Git LFS 또는 외부 스토리지(S3 등)에 저장하고 경로만 커밋.

## 벤치마크 대상/메트릭 확장
- 환각 외에 추론 오류/도구 실패/hand-off를 측정하려면 추가 필드를 정의하고 해당 detector가 읽을 수 있도록 구현.
- 메트릭은 detector가 반환하는 `DetectionResult.details`에 자유롭게 기록 후 리포트 단계에서 집계.
