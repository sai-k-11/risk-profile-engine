from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, conint, confloat, field_validator

class RiskProfile(str):
    # keep same labels as before
    CONSERVATIVE = "Conservative"
    MODERATE = "Moderate"
    AGGRESSIVE = "Aggressive"
    
CRYPTO_INTEREST = {
    0: 'Store of value ("Digital Gold"/ hedge against fiat debasement).',
    1: "Diversification from traditional equity/bond correlations.",
    2: 'Direct exposure to the "Future of Finance" (Web3, DeFi, RWA- tokenized stocks, real estate, bonds).',
    3: "Speculative growth (high risk/high reward).",
}

NET_WORTH_ALLOCATION = {
    0: "< 1% (Testing the waters)",
    1: "1-5% (Institutional standard)",
    2: "5-10% (Aggressive/Strategic)",
    3: "10%+ (High conviction/Crypto-native)",
}

HOLDING_PERIOD = {
    0: "Tactical (1-2 years).",
    1: "Mid-term (3-5 years).",
    2: "Legacy/Intergenerational (5+ years).",
}

THEMES = {
    0: "Real World Assets Tokenization: (e.g., Tokenized stocks, treasury bills, real estate, or private credit).",
    1: "AI x Crypto: (Decentralized compute and AI agents).",
    2: "Infrastructure: (Layer 1 and Layer 2 scaling solutions).",
    3: "Yield Generation: (Staking and institutional DeFi).",
    4: "Not sure, open for recommendation",
}

CRASH_REACTION = {
    0: "Liquidate immediately to protect remaining capital.",
    1: "Maintain the position and wait for a recovery.",
    2: 'Aggressively "buy the dip" to lower the cost basis.',
    3: "Let the algo decide (stick to the backtested plan)",
}

DRAWDOWN_PAIN = {
    0: ">20%",
    1: ">30%",
    2: ">50%",
    3: "% drawdown has no impact",
}

EXPECTED_RETURN = {
    0: "12% to 24%",
    1: "24% to 36%",
    2: ">36%",
}

def _validate_code(v: Any, allowed: Dict[int, str], field_name: str) -> int:
    if isinstance(v, bool):
        raise ValueError(f"{field_name} must be an integer code, not true/false.")
    if isinstance(v, int):
        if v in allowed:
            return v
        raise ValueError(f"{field_name} must be one of {sorted(allowed.keys())}.")
    raise ValueError(f"{field_name} must be an integer code like {sorted(allowed.keys())}.")

class QuestionnaireInput(BaseModel):
    crypto_interest: conint(ge=0, le=3) = Field(..., description="Code 0-3 (see codebook)")
    net_worth_allocation: conint(ge=0, le=3) = Field(..., description="Code 0-3 (see codebook)")
    holding_period: conint(ge=0, le=2) = Field(..., description="Code 0-2 (see codebook)")
    themes: Optional[List[conint(ge=0, le=4)]] = Field(default_factory=list, description="List of codes 0-4")
    reaction_to_50pct_drop: conint(ge=0, le=3) = Field(..., description="Code 0-3 (see codebook)")
    drawdown_pain: conint(ge=0, le=3) = Field(..., description="Code 0-3 (see codebook)")
    expected_annual_return: conint(ge=0, le=2) = Field(..., description="Code 0-2 (see codebook)")

    @field_validator("crypto_interest")
    @classmethod
    def _v_crypto_interest(cls, v): return _validate_code(v, CRYPTO_INTEREST, "crypto_interest")

    @field_validator("net_worth_allocation")
    @classmethod
    def _v_networth(cls, v): return _validate_code(v, NET_WORTH_ALLOCATION, "net_worth_allocation")

    @field_validator("holding_period")
    @classmethod
    def _v_holding(cls, v): return _validate_code(v, HOLDING_PERIOD, "holding_period")

    @field_validator("reaction_to_50pct_drop")
    @classmethod
    def _v_reaction(cls, v): return _validate_code(v, CRASH_REACTION, "reaction_to_50pct_drop")

    @field_validator("drawdown_pain")
    @classmethod
    def _v_drawdown(cls, v): return _validate_code(v, DRAWDOWN_PAIN, "drawdown_pain")

    @field_validator("expected_annual_return")
    @classmethod
    def _v_return(cls, v): return _validate_code(v, EXPECTED_RETURN, "expected_annual_return")

    @field_validator("themes")
    @classmethod
    def _v_themes(cls, v):
        if v is None:
            return []
        if not isinstance(v, list):
            raise ValueError("themes must be a list of integer codes.")
        for t in v:
            _validate_code(t, THEMES, "themes item")
        return v

class RiskProfileResponse(BaseModel):
    risk_profile: str
    risk_score: conint(ge=0, le=100)
    confidence: confloat(ge=0, le=1)
    reasons: List[str]
    score_breakdown: dict
