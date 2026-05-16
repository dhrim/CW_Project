# Echo Adapter Benchmark Bundle

| 벤치마크 | 세션 수 | 플래그 | 메트릭 | 세부 보고서 |
| --- | --- | --- | --- | --- |
| hallucination | 3 | 2 | token_overlap | [benchmark/methodology/README.md#1-환각-탐지-hallucination](hallucination/README.md) |
| reasoning | 2 | 1 | constraint_coverage | [benchmark/methodology/README.md#2-추론-오류-reasoning-errors](reasoning/README.md) |
| tool-failure | 2 | 1 | tool_failure_count | [benchmark/methodology/README.md#3-도구-사용-실패-tool-failures](tool-failure/README.md) |
| handoff | 2 | 1 | handoff_slot_coverage | [benchmark/methodology/README.md#4-handoff-실패](handoff/README.md) |

## 총괄 요약
- 총 세션 수: 9
- 총 플래그: 5
- 어댑터: models.base_adapter:EchoAdapter

각 세부 벤치마크 폴더에서 상세 보고서를 확인할 수 있습니다.