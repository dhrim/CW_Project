# Benchmark Methodology & Metrics

## 1. 환각 탐지 (Hallucination)
- **Detector:** `SimpleHallucinationDetector`
- **Method:** Token overlap ratio between `reference_facts` and `model_output`.
- **Primary Metric:** Overlap score (0~1). Flagged as hallucination when score < threshold.
- **Supporting Docs:** [Hallucination Survey](../research/surveys/01-agent-error-detection-survey.md)

## 2. 추론 오류 (Reasoning Errors)
- _준비 중_: CoT consistency 평가, KPI constraint 검증 등. 결과가 정리되는 대로 이 문서에 추가.

## 3. 도구 사용 실패 (Tool Failures)
- _준비 중_: ToolBench/ToolEmu 스타일 실행 로그 분석.

## 4. Handoff 실패
- _준비 중_: context transfer completeness, timeout, conflict 지표.

각 탐지기는 해당 섹션을 참조해 구현 방식을 문서화하고, 실행 보고서에서는 이 문서의 링크를 통해 세부 내용을 확인할 수 있도록 합니다.
