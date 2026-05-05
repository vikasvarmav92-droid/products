from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class ProductOpportunity(Base):
    __tablename__ = "product_opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    query: Mapped[str] = mapped_column(String(255), index=True)
    product_name: Mapped[str] = mapped_column(String(255), index=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    supplier_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    supplier_price_nzd: Mapped[float] = mapped_column(Float)
    shipping_cost_nzd: Mapped[float] = mapped_column(Float)
    shipping_days_estimate: Mapped[int] = mapped_column(Integer)
    supplier_rating: Mapped[float] = mapped_column(Float)

    estimated_sell_price_nzd: Mapped[float] = mapped_column(Float)
    estimated_gross_margin_nzd: Mapped[float] = mapped_column(Float)
    estimated_margin_pct: Mapped[float] = mapped_column(Float)

    landed_cost_nzd: Mapped[float] = mapped_column(Float)
    gst_estimate_nzd: Mapped[float] = mapped_column(Float)
    levy_estimate_nzd: Mapped[float] = mapped_column(Float)
    payment_fee_nzd: Mapped[float] = mapped_column(Float)
    return_allowance_nzd: Mapped[float] = mapped_column(Float)

    demand_score: Mapped[float] = mapped_column(Float)
    competition_score: Mapped[float] = mapped_column(Float)
    risk_score: Mapped[float] = mapped_column(Float)
    social_score: Mapped[float] = mapped_column(Float)
    final_opportunity_score: Mapped[float] = mapped_column(Float)

    ai_recommendation: Mapped[str] = mapped_column(Text)
    raw_signals: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
