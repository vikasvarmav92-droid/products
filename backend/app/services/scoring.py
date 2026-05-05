def clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def score_product(*, demand_growth: float, social_growth: float, supplier_cost: float, shipping_days: int, supplier_rating: float, competition: float, margin_pct: float, risk: float) -> float:
    demand_component = clamp(demand_growth)
    social_component = clamp(social_growth)
    cost_component = clamp(100 - supplier_cost)
    shipping_component = clamp(100 - (shipping_days * 2.2))
    rating_component = clamp((supplier_rating / 5) * 100)
    competition_component = clamp(100 - competition)
    margin_component = clamp(margin_pct)
    risk_component = clamp(100 - risk)

    weighted = (
        demand_component * 0.18
        + social_component * 0.14
        + cost_component * 0.10
        + shipping_component * 0.08
        + rating_component * 0.10
        + competition_component * 0.15
        + margin_component * 0.18
        + risk_component * 0.07
    )
    return round(clamp(weighted), 2)
