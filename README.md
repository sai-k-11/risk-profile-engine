# Risk Profile Engine (Explainable AI)

A small, explainable "AI engine" that ingests investor questionnaire responses and returns:
- Risk profile label (Conservative / Moderate / Aggressive)
- Risk score (0–100)
- Confidence (heuristic)
- Reasons + score breakdown (auditability)

## Tech
- Python + FastAPI
- Pydantic validation
- Swagger UI at /docs

## Run locally (Mac)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
