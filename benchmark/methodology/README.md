# Benchmark Methodology & Metrics

## 1. 환각 탐지 (Hallucination)
- **Detector:** `SimpleHallucinationDetector`
- **Method:** Token overlap ratio between `reference_facts` and `model_output`.
- **Primary Metric:** Overlap score (0~1). Flagged as hallucination when score < threshold.
- **Supporting Docs:** [Hallucination Survey](../research/surveys/01-agent-error-detection-survey.md)

## 2. 추론 오류 (Reasoning Errors)
- **Detector:** `ReasoningConsistencyDetector`
- **Method:** Compare `required_constraints` vs `satisfied_constraints` to detect missing steps.
- **Metric:** `constraint_coverage` (missing constraints list). Flagged if any required constraint absent.
- **References:** ODCV-Bench, chain-of-thought coverage literature (see `research/surveys/01-agent-error-detection-survey.md`).

## 3. 도구 사용 실패 (Tool Failures)
- **Detector:** `ToolFailureDetector`
- **Method:** Count tool calls whose `status` != `success`; flag if failures exceed threshold.
- **Metric:** `tool_failure_count`.
- **References:** ToolEmu, SafeToolBench (see `research/surveys/02-benchmark-datasets-survey.md`).

## 4. Handoff 실패
- **Detector:** `HandoffIntegrityDetector`
- **Method:** Compare required handoff slots (context fields) with delivered slots; flag missing ones.
- **Metric:** `handoff_slot_coverage`.
- **References:** LangChain observability docs, OpenAI Agents handoff guidelines.

각 탐지기는 해당 섹션을 참조해 구현 방식을 문서화하고, 실행 보고서에서는 이 문서의 링크를 통해 세부 내용을 확인할 수 있도록 합니다.
