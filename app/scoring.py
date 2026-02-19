from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List

from .models import (
    QuestionnaireInput,
    CRYPTO_INTEREST,
    NET_WORTH_ALLOCATION,
    HOLDING_PERIOD,
    THEMES,
    CRASH_REACTION,
    DRAWDOWN_PAIN,
    EXPECTED_RETURN,
)

@dataclass
class ScoringResult:
    profile: str
    score: int
    confidence: float
    reasons: List[str]
    breakdown: Dict[str, int]

def clamp(n: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, n))

def score_risk_profile(data: QuestionnaireInput) -> ScoringResult:
    breakdown: Dict[str, int] = {}
    reasons: List[str] = []
    score = 0

    # 1) Allocation (0-3)
    if data.net_worth_allocation == 0:
        pts = 2
        reasons.append("Allocation <1% indicates testing the waters (lower risk appetite).")
    elif data.net_worth_allocation == 1:
        pts = 8
        reasons.append("Allocation 1–5% aligns with institutional standard (moderate risk).")
    elif data.net_worth_allocation == 2:
        pts = 15
        reasons.append("Allocation 5–10% suggests aggressive/strategic exposure (higher risk).")
    else:
        pts = 22
        reasons.append("Allocation 10%+ suggests high conviction/crypto-native (high risk appetite).")
    breakdown["allocation"] = pts
    score += pts

    # 2) Crash reaction (0-3)
    if data.reaction_to_50pct_drop == 0:
        pts = 0
        reasons.append("Liquidating immediately suggests low tolerance for volatility.")
    elif data.reaction_to_50pct_drop == 1:
        pts = 10
        reasons.append("Holding through a 50% drop suggests moderate tolerance for volatility.")
    elif data.reaction_to_50pct_drop == 2:
        pts = 18
        reasons.append('Buying the dip suggests strong tolerance for drawdowns (higher risk).')
    else:
        pts = 14
        reasons.append("Letting the algo decide suggests discipline with a system (moderate-to-high risk).")
    breakdown["crash_reaction"] = pts
    score += pts

    # 3) Drawdown pain (0-3)
    if data.drawdown_pain == 0:
        pts = 6
        reasons.append("Pain threshold at >20% indicates moderate sensitivity to losses.")
    elif data.drawdown_pain == 1:
        pts = 10
        reasons.append("Pain threshold at >30% indicates moderate-to-higher tolerance.")
    elif data.drawdown_pain == 2:
        pts = 16
        reasons.append("Pain threshold at >50% indicates high tolerance for volatility.")
    else:
        pts = 20
        reasons.append("No impact from drawdown suggests very high tolerance for volatility.")
    breakdown["drawdown_pain"] = pts
    score += pts

    # 4) Expected return (0-2)
    if data.expected_annual_return == 0:
        pts = 6
        reasons.append("Expected return 12–24% aligns with moderate expectations.")
    elif data.expected_annual_return == 1:
        pts = 12
        reasons.append("Expected return 24–36% aligns with higher risk expectations.")
    else:
        pts = 18
        reasons.append("Expected return >36% implies aggressive expectations (higher risk).")
    breakdown["expected_return"] = pts
    score += pts

    # 5) Holding period (0-2)
    if data.holding_period == 0:
        pts = 4
        reasons.append("Tactical 1–2 year horizon suggests less time to recover from volatility.")
    elif data.holding_period == 1:
        pts = 8
        reasons.append("Mid-term 3–5 year horizon supports moderate risk capacity.")
    else:
        pts = 12
        reasons.append("Legacy 5+ year horizon supports higher risk capacity (more recovery time).")
    breakdown["holding_period"] = pts
    score += pts

    # 6) Interest type (0-3)
    if data.crypto_interest == 3:
        pts = 14
        reasons.append("Speculative growth preference indicates higher risk preference.")
    elif data.crypto_interest == 0:
        pts = 6
        reasons.append("Store-of-value preference indicates more conservative positioning.")
    elif data.crypto_interest == 1:
        pts = 8
        reasons.append("Diversification motive indicates balanced risk intent.")
    else:  # 2
        pts = 10
        reasons.append("Future-of-finance exposure indicates moderate-to-higher risk preference.")
    breakdown["interest_style"] = pts
    score += pts

    score = int(clamp(score, 0, 100))

    if score <= 35:
        profile = "Conservative"
    elif score <= 70:
        profile = "Moderate"
    else:
        profile = "Aggressive"

    boundaries = [35, 70]
    distance = min(abs(score - b) for b in boundaries)
    confidence = clamp(0.55 + (distance / 100.0), 0.55, 0.90)

    return ScoringResult(
        profile=profile,
        score=score,
        confidence=float(confidence),
        reasons=reasons,
        breakdown=breakdown,
    )
