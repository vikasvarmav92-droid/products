from datetime import datetime

from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=255)
    max_products: int = Field(default=20, ge=1, le=100)


class ProductOpportunityOut(BaseModel):
    id: int
    query: str
    product_name: str
    image_url: str | None
    supplier_url: str | None
    supplier_price_nzd: float
    shipping_cost_nzd: float
    shipping_days_estimate: int
    estimated_sell_price_nzd: float
    estimated_gross_margin_nzd: float
    estimated_margin_pct: float
    demand_score: float
    competition_score: float
    risk_score: float
    social_score: float
    final_opportunity_score: float
    ai_recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True
