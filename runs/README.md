# Runs & PoC 기록
- 이 폴더에는 벤치마킹 실행 결과(로그, 리포트, 전체 응답 아티팩트)를 날짜별로 보관합니다.
- 폴더명 권장 형식: `runs/YYYY-MM-DD-<benchmark>-<model>/`
- 실행 예시:
  ```bash
  cd benchmark
  python evaluation/run_benchmark.py data/<dataset>.jsonl \
    --adapter models.base_adapter:EchoAdapter \
    --detector detectors.hallucination:SimpleHallucinationDetector \
    --report ../runs/2026-05-17-hallucination-run/report.json
  ```
- 각 폴더에는 최소한 `README.md`(요약/메타 링크), `run.log`(콘솔 출력), `artifacts/`(전체 호출/응답 JSONL), `report.json`(요약/메트릭/메타데이터)을 포함하세요.
