# 02. 에이전트 오류 벤치마크용 표준 데이터셋 서베이
작성 시각: 2026-05-17 04:45 KST

> 목적: 환각·추론 오류·도구 실패·handoff 실패 탐지를 위한 대표 공개 데이터셋/벤치마크를 한눈에 정리하고, 부족한 영역은 구축 방안을 제안한다.

## 1. 환각(Hallucination) 탐지용 데이터셋
| 데이터셋 | 규모/특징 | 커버 범위 | 참고 |
| --- | --- | --- | --- |
| **HaluEval (2023, EMNLP)** | 5,000 일반 쿼리 + 30,000 작업별 샘플 (QA, 지식 기반 대화, 요약). ChatGPT 응답과 인간 주석 포함. | 자연어 QA, 요약, 대화 환각. | [GitHub: RUCAIBox/HaluEval](https://github.com/RUCAIBox/HaluEval) |
| **SHROOM (SemEval-2024 Task 6)** | 4,000 출력 × 5인 라벨, 3개 작업(MT/Paraphrase/Definition). 모델-aware vs agnostic 트랙 + 정답/캘리브레이션 평가. | 문장 수준 환각 + 모델 정보 여부에 따른 시나리오. | [arXiv:2403.07726](https://arxiv.org/html/2403.07726v3) |
| **RAGTruth / FActScore / TruthfulQA** | RAGTruth: Retrieval-grounded QA 18K claim 단위. FActScore: wiki 증거 기반 문장 정합성. TruthfulQA: 817 질문 × 다중 레퍼런스. | RAG/사실 검증 중심 환각. Cognometry v0가 8개 벤치마크 교차검증에 활용. | [Cognometry v0 설명](https://github.com/EdinburghNLP/awesome-hallucination-detection) |
| **Deep Research Trajectory 평가 (2026)** | Claim / Noise / Action / Restriction 4가지 환각 범주에 대해 세션 로그 단위 라벨. | 다중 단계 조사형 에이전트. | [arXiv:2601.22984](https://arxiv.org/html/2601.22984) |

**공백**: handoff/도구 호출이 얽힌 환각 로그는 거의 없음. 필요 시 ToolEmu·LangGraph 로그와 결합한 합성 데이터가 요구됨.

## 2. 추론 오류·제약 위반 데이터셋
| 데이터셋 | 규모/특징 | 커버 범위 | 참고 |
| --- | --- | --- | --- |
| **ODCV-Bench (2025)** | 40 시나리오 × Mandated/Incentivized 변형. KPI 압박 상황에서 12개 LLM 평가(위반율 1.3~71.4%). | KPI-driven constraint violation, 윤리·법 준수 여부. | [arXiv:2512.20798](https://arxiv.org/html/2512.20798v1) |
| **MAST Failure Taxonomy 데이터 (2025)** | 1,642 실행 트레이스, 14 세부 실패 모드. 조정 실패 36.9%로 최다. | 멀티에이전트 시스템 전반 실패 라벨. | [arXiv:2503.13657](https://arxiv.org/html/2503.13657v1) |
| **DeepMind Multi-Agent Reliability 실험 (2025)** | 180 구성 × 5 아키텍처 × 3 LLM. 구조화되지 않은 네트워크에서 단일 대비 최대 17.2배 오류. | 에이전트 수·토폴로지 대비 성능 데이터. | [The Multi-Agent Trap](https://towardsdatascience.com/the-multi-agent-trap/) |

**공백**: 일반화된 reasoning error 라벨(예: Chain-of-Thought constraint violation, math/logic 실패)을 멀티에이전트 로그와 연결한 공개 세트는 부족. 필요 시 CoT 그래프/제약을 자동 추출하는 파이프라인 구축이 필요.

## 3. 도구 사용 실패·안전 데이터셋
| 데이터셋 | 규모/특징 | 커버 범위 | 참고 |
| --- | --- | --- | --- |
| **ToolBench (2023~)** | RapidAPI 기반 16,464 API, 120K instruction-API pair. Pass Rate, Win Rate, AST 정확도 제공. StableToolBench/ToolBench-V/UltraTool로 품질·안전 강화. | 다중 API 계획/실행 정확도 + 복구 능력. | [EmergentMind 정리](https://www.emergentmind.com/topics/toolbench-evaluation) |
| **ToolEmu (ICLR 2024)** | 36 툴킷/311 툴/144 고위험 시나리오. GPT-4 샌드박스 + LM 기반 Safety evaluator, 인적 검증 시 68.8% 실제 위험과 일치. | 도구 실행 실패, 안전 위험 탐지. | [GitHub: ryoungj/ToolEmu](https://github.com/ryoungj/ToolEmu) |
| **SafeToolBench (2025)** | Prospective 평가. User Instruction/Tool/Joint 3축 × 9 세부 위험 차원. SafeInstructTool 프레임워크로 사전 경고 정확도 향상. | 실행 전 위험 평가(송금, 이메일 등 고위험 도구). | [arXiv:2509.07315](https://arxiv.org/html/2509.07315v1) |
| **AgentSafetyBench / R-Judge / ToolScan taxonomy** | ToolScan: 7가지 오류 패턴(도구 선택 실패, 파라미터 오류, 반복 루프 등) 보고. AgentSafetyBench·R-Judge는 ToolEmu 후속 안전 평가. | 세부 도구 실패 유형 라벨. | [SafeToolBench 본문 및 관련 인용] |

**공백**: 실제 생산 로그 기반 공개 데이터는 보안상 부재. SafeToolBench/ToolEmu가 합성·모사 데이터인 만큼, 사용자 정의 API/프롬프트를 반영한 Organization-specific 데이터 파이프라인 필요.

## 4. Handoff 실패·관측 데이터셋
- **현재 표준 부재**: OpenAI Agents SDK 문서는 handoff를 "툴"로 모델링하고 입력 스키마/`on_handoff` 후크 제공하지만, 실패 라벨이 붙은 공개 데이터셋은 없음. [문서](https://openai.github.io/openai-agents-python/handoffs/)
- **운영 가이드**: LangChain `Agent Observability` 글은 멀티에이전트 추적 필요성과 로그 항목(툴 호출, 프롬프트 버전, 컨텍스트)을 정의하지만 데이터셋 형태가 아니라 모범 사례. [LangChain 기사](https://www.langchain.com/articles/agent-observability)
- **MAST/DeepMind** 결과를 handoff 라벨로 재가공 가능**하나**, 세부적으로 "어느 handoff에서 무슨 컨텍스트가 손실되었는지" 묘사된 로그는 없음.

### 4.1 구축 방안 제안 (Handoff/조정 실패 데이터)
1. **프레임워크 Instrumentation**: LangGraph/LangChain + OpenTelemetry를 이용해 `handoff_id`, 전달 context hash, 수신 agent 상태를 JSONL로 저장.
2. **시나리오 템플릿**: 지원/헬프데스크/triage 등 실제 업무 플로우를 3~4 agent로 구성, 정상/실패 변형을 자동 생성 (예: context slot 누락, tool-call 미완료, 반대 지시 충돌 등).
3. **자동 라벨링 규칙**:
   - Context Diff: handoff 입력 대비 출력에서 필요한 슬롯이 사라지면 `handoff_context_loss`.
   - Response SLA 위반: handoff 후 응답 지연/미완료는 `handoff_timeout`.
   - 충돌 탐지: 수신 agent가 이전 agent 지시를 덮어쓰면 `handoff_conflict`.
4. **체크리스트 기반 휴먼 검수**: 10% 샘플은 사람이 확인해 heuristic 오탐을 줄임.
5. **공개 가능 버전**: 고객 데이터 제거 후 synthetic user/task만 남겨 배포.

## 5. 정리 및 다음 단계
- 환각·도구 실패는 비교적 풍부한 공개 데이터가 있으므로, **과제에 필요한 네 가지 오류 중 handoff/조정 부분**이 가장 큰 공백.
- 다음 액션으로는 (a) ToolScan taxonomy 원문 세부 내용 수집, (b) handoff synthetic 로그 생성 스크립트 설계, (c) 조직-specific 데이터셋 요구사항 정의가 필요.
- 모든 새 문서는 `NN-` 접두사로 버전 관리 (예: 이번 문서는 `02-...`). 기존 `01-agent-error-detection-survey.md`도 같은 규칙으로 리네이밍 완료.
