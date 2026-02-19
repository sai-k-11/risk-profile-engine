from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import QuestionnaireInput, RiskProfileResponse
from .scoring import score_risk_profile

app = FastAPI(
    title="Risk Profile Engine",
    version="1.0.0",
    description="Accepts questionnaire form data and returns an explainable investor risk profile."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/v1/risk-profile",
    response_model=RiskProfileResponse,
    description=(
        "Try different options related to your money to see how the user's risk profile changes. "
        "This endpoint accepts input via the request body, not via URL parameters."
    )
)
def risk_profile(data: QuestionnaireInput):
    result = score_risk_profile(data)
    return RiskProfileResponse(
        risk_profile=result.profile,
        risk_score=result.score,
        confidence=result.confidence,
        reasons=result.reasons,
        score_breakdown=result.breakdown,
    )

@app.get("/v1/risk-profile", include_in_schema=False)
def risk_profile_get_help():
    return {
        "message": "This endpoint requires POST. Open /docs and use 'Try it out' to submit JSON."
    }
