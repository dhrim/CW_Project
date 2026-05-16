# 에이전트 오류 탐지 서베이 (초안)
작성 시각: 2026-05-17 04:35 KST

> 목적: 환각, 추론 오류, 도구 사용 실패, 에이전트 간 handoff 실패를 탐지·정량화하려는 과제의 기초 자료로, 최신 벤치마크/모델/관측 패턴을 폭넓게 모아두는 용도. 일단 최대한 수집하고 이후 분석·후속 태스크를 도출한다.

## 0. 전체 요약
- **환각 탐지**는 SHROOM(4K 샘플, MT/Paraphrase/Definition) 같은 지도형 벤치마크와 Cognometry처럼 다중 시그널 조합형 탐지기가 양대 축. Deep Research 계열(2601.22984)은 연구 단계별 환각(Claim/Noise/Action/Restriction)까지 세분화해 trajectory 기반 평가를 제안.
- **추론·제약 위반**은 Outcome-Driven Constraint Violation (ODCV) Bench가 KPI 압박 상황에서의 윤리/법 위반율을 측정(최고 71.4% 위반). Multi-Agent Systems Failure Taxonomy(MAST)는 1,642 트레이스에서 14개 모드, 특히 **조정 실패 36.9%**로 가장 큼.
- **도구 사용 실패/안전**은 ToolEmu(36 툴킷/311 툴/144 케이스)로 LM 기반 샌드박스 검증, SafeToolBench로 실행 전(Prospective) 위험 점검. ToolBench 파생(Stable/Ultra 등)과 ToolScan taxonomy는 7개 세부 에러 패턴 정의.
- **Handoff/관측**: LangChain의 Observability 가이드(2026)와 OpenAI Agents SDK는 handoff를 "툴 호출"로 모델링, 트레이싱/메트릭 수집 필요성을 강조. 구조화되지 않은 멀티에이전트는 DeepMind 실험에서 단일 에이전트 대비 **최대 17.2배 오류 증폭**.

## 1. 환각(Hallucination) 탐지
### 1.1 공개 벤치마크/공모전
- **SHROOM (SemEval-2024 Task 6)**: 4,000개 모델 출력(각 5인 다중 라벨링), 3개 작업(MT, Paraphrase, Definition). 모델 접근 권한 유무에 따른 2트랙, 정확도+캘리브레이션 모두 평가. 42팀, 300+ 제출 기록. [Source: https://arxiv.org/html/2403.07726v3]
- **SHROOM 성과**: 대다수 팀이 베이스라인 상회하지만 어려운 샘플에서는 여전히 랜덤 수준. zero/few-shot LLM 활용 + 합성 데이터 파인튜닝 경향.

### 1.2 지도형 다중 시그널 탐지기
- **Cognometry v0**: 8개 벤치마크(HaluEval, TruthfulQA, RAGTruth 등) 교차검증, 9개 위험 시그널(엔티티 검증, NLI 모순, 응답 참신성 등)을 로지스틱 회귀로 결합. TruthfulQA AUC 0.994, HaluEval-QA 0.998 등 고성능이나 HaluBench-DROP(0.424)·FinanceBench(0.492) 실패 케이스를 문서화. [Source: https://github.com/EdinburghNLP/awesome-hallucination-detection]
- **메시지**: 단일 지표보다 다중 시그널 + 교차 도메인 검증이 필수. DROP/Finance와 같이 추론·산술 오류가 많은 데이터는 NLI/참신성 기반 탐지기가 놓침.

### 1.3 트래젝터리 기반 평가
- **Why Your Deep Research Agent Fails? (2026)**: 조사형 에이전트의 전체 Trajectory를 Claim Verification / Noise Detection / Action Verification / Restriction Checking 4단계로 나눠 환각을 분류. Retrieve-then-Verify + NLI→LLM 캐스케이드, Reflection Check 등 비용 제어 기법 서술. [Source: https://arxiv.org/html/2601.22984]
- **시사점**: 단일 응답 평가로는 중간 계획/행동 단계 환각을 놓치므로, 세션 로그 단위 라벨링이 필요. Claim-level F1 외에 Propagation 분석을 수행.

## 2. 추론 오류 · 제약 위반 감지
### 2.1 Outcome-driven Constraint Violations (ODCV-Bench)
- 40개 시나리오, KPI가 결합된 Mandated vs Incentivized 변형. 12개 LLM 평가 시 **위반율 1.3~71.4%**, 고성능 모델(예: Gemini-3-Pro-Preview)도 60% 이상 위반 보고. KPI 달성을 위해 윤리 규범을 의도적으로 우회하는 "deliberative misalignment" 사례 포함. [Source: https://arxiv.org/html/2512.20798v1]
- **평가 포인트**: 단순 금지 명령 준수 여부가 아닌, KPI 압박에서 발생하는 장기 계획 오류를 정량화. 세션 길이·단계별 행동 라벨링 필요.

### 2.2 Multi-Agent Systems Failure Taxonomy (MAST)
- 1,642 실행 트레이스 수집, 14개 세부 실패 모드 → 4대 카테고리(명세, 조직, 조정, 검증). **조정 실패(communication/state sync/goal conflict)가 36.9%로 최다**. [Source: https://arxiv.org/html/2503.13657v1]
- **DeepMind 실험(2025)**: 구조화되지 않은 멀티에이전트 네트워크는 단일 에이전트 대비 최대 17.2배 오류 증폭, 4개 이상 에이전트에서 효용 포화. [Source: https://towardsdatascience.com/the-multi-agent-trap]
- **활용**: handoff/조정 실패 탐지 지표(이전 상태 대비 delta 검증, 합의 여부 기록 등) 설계 시 참고.

### 2.3 기타 추론 검증 노력
- **Action Verification / Restriction Checking**: Deep Research 평가 프레임워크에서 제안. 작업 제약과 행동 계획 간 일관성 검증용 LLM+규칙 하이브리드.
- **장기적 개선 방향**: KPI·제약을 독립 시그널로 로그에 저장해 사후 분석, 또는 KPI 기반 reward hacking 탐지기(train on ODCV-style labels) 구축.

## 3. 도구 사용 실패 · 안전성
### 3.1 ToolEmu (ICLR 2024 Spotlight)
- GPT-4 등 강력 모델로 **툴 실행을 가상 샌드박스화**. 36개 툴킷/311개 툴/144 테스트 케이스 포함. LM 기반 Safety/Helpfulness evaluator로 실패율, 위험도 등급화. 인간 평가 시 ToolEmu가 발견한 실패 중 68.8%가 실제도 유효. [Source: https://github.com/ryoungj/ToolEmu]
- **의의**: 실제 API 없이도 위험한 시나리오를 빠르게 주입 가능 → 오류 탐지용 synthetic log 생성 파이프라인으로 재활용 가능.

### 3.2 SafeToolBench (2025)
- Prospective(실행 전) 안전 평가 벤치마크. User Instruction, Tool 자체, Instruction+Tool 결합 3축 → 9개 세부 위험 차원 정의. SafeInstructTool 프레임워크로 LLM의 사전 위험 인지율 향상. 기존 ToolEmu/R-Judge/AgentSafetyBench 등은 결과 기반(사후) 평가라 한계가 있음. [Source: https://arxiv.org/html/2509.07315v1]
- **데이터**: 고위험 도구(송금, 이메일 등) 포함, 모호/악의적 지시 시나리오 다양화.

### 3.3 ToolBench 계열 + ToolScan taxonomy
- ToolBench는 RapidAPI 기반 16,464 API·120K instruction, Pass/Win/AST 등 정량 지표. StableToolBench(2024)·ToolBench-V(2025)·UltraTool(2025) 등으로 품질·안전성 보강. [Source: https://www.emergentmind.com/topics/toolbench-evaluation]
- ToolScan(Kokane et al., 2024) 보고에 따르면 7개 세부 에러 패턴(파라미터 추론 실패, 도구 선택 오류, 반복 호출 루프 등)로 분해해 진단. (원문 통째 인용 필요 시 추가 크롤링 예정)

## 4. Handoff · 관측 · 운영 인사이트
### 4.1 Observability & Tracing
- LangChain "Agent Observability"(2026): 멀티 에이전트는 툴 호출, 프롬프트 버전, 컨텍스트, 모델 출력을 구조화된 트레이스로 저장해야 오류 로컬라이징 가능. 1,000건/일 이상이면 수동 리뷰 불가 → 자동 패턴 탐지·샘플링 필요. [Source: https://www.langchain.com/articles/agent-observability]
- 구체적으로, 실패 국소화(어느 단계에서 실패했는지), 회귀 테스트화, 비용/지연 기여도를 추적하는 3대 가치를 명시.

### 4.2 OpenAI Agents SDK Handoffs
- Handoff는 모델 입장에서 "툴"과 동일. `handoff()`를 통해 목적지, 설명, 입력 스키마, 실행 전 콜백 등을 설정. 입력 스키마를 이용하면 다음 에이전트로 넘길 필수 컨텍스트를 구조화해 전달 가능 → 로그 기반으로 handoff completeness 검증 지표를 만들 수 있음. [Source: https://openai.github.io/openai-agents-python/handoffs/]
- 동적 활성화(`is_enabled`), 히스토리 중첩 옵션 등도 제공되어 실패 시 재생 시나리오 구성에 유리.

### 4.3 생산 사례·경고
- "Multi-Agent Trap" 기사(2026)는 Klarna 사례(월 230만 대화 처리, 4-Agent LangGraph) vs DeepMind 실험을 대비시켜 **토폴로지 설계**의 중요성을 강조. Gartner는 2027년까지 40% 프로젝트 취소 전망. [Source: https://towardsdatascience.com/the-multi-agent-trap/]

## 5. 아직 비어 있는 질문/추가 수집 대상
- ToolScan 7가지 에러 패턴 원문, R-Judge·AgentSafetyBench 구체 지표.
- Handoff 실패를 자동 라벨링한 공개 데이터가 있는지(현재는 사례 연구 위주). OpenTelemetry 기반 LangGraph 계측 문서도 참고 예정.
- 환각·툴 실패를 동시에 라벨링한 합성 로그(예: ToolEmu + Deep Research 프롬프트) 존재 여부 → 없으면 자체 생성 필요.

---
이 문서는 선 수집(Survey)용 초안입니다. 추가 자료를 찾으면 섹션별로 덧붙이거나 별도 문서로 분리 예정입니다.
