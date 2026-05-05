from sqlalchemy.orm import Session

from app.models.product_opportunity import ProductOpportunity
from app.providers.base.interfaces import MarketplaceProvider, SocialProvider, SupplierProvider, TrendsProvider
from app.services.scoring import score_product


class OpportunityScannerService:
    def __init__(self, trends: TrendsProvider, social: SocialProvider, market: MarketplaceProvider, supplier: SupplierProvider):
        self.trends = trends
        self.social = social
        self.market = market
        self.supplier = supplier

    def expand_query(self, query: str) -> list[str]:
        return [query, f"{query} for home", f"portable {query}", f"eco {query}"]

    def calculate_landed_cost(self, product_cost: float, shipping_cost: float) -> dict[str, float]:
        subtotal = product_cost + shipping_cost
        gst = subtotal * 0.15
        levy = subtotal * 0.03
        payment_fee = subtotal * 0.029
        return_allowance = subtotal * 0.05
        landed = subtotal + gst + levy + payment_fee + return_allowance
        return {
            "landed": round(landed, 2),
            "gst": round(gst, 2),
            "levy": round(levy, 2),
            "payment_fee": round(payment_fee, 2),
            "return_allowance": round(return_allowance, 2),
        }

    def scan(self, db: Session, query: str, max_products: int) -> list[ProductOpportunity]:
        ideas = self.expand_query(query)
        opportunities: list[ProductOpportunity] = []

        for idea in ideas:
            demand = self.trends.get_demand(idea)
            social = self.social.get_social_signal(idea)
            market = self.market.get_market_signal(idea)

            for supply in self.supplier.search_products(idea, max_products // len(ideas) + 1):
                landed = self.calculate_landed_cost(supply.product_cost_nzd, supply.shipping_cost_nzd)
                sell_price = market.avg_price_nzd
                gross_margin = sell_price - landed["landed"]
                margin_pct = (gross_margin / sell_price * 100) if sell_price else 0
                risk_score = max(0, min(100, (supply.shipping_days * 1.4) + ((4.2 - supply.supplier_rating) * 15)))

                final_score = score_product(
                    demand_growth=demand.momentum_score,
                    social_growth=social.engagement_score,
                    supplier_cost=supply.product_cost_nzd,
                    shipping_days=supply.shipping_days,
                    supplier_rating=supply.supplier_rating,
                    competition=market.competition_score,
                    margin_pct=margin_pct,
                    risk=risk_score,
                )

                record = ProductOpportunity(
                    query=query,
                    product_name=supply.product_name,
                    image_url=supply.image_url,
                    supplier_url=supply.supplier_url,
                    supplier_price_nzd=supply.product_cost_nzd,
                    shipping_cost_nzd=supply.shipping_cost_nzd,
                    shipping_days_estimate=supply.shipping_days,
                    supplier_rating=supply.supplier_rating,
                    estimated_sell_price_nzd=round(sell_price, 2),
                    estimated_gross_margin_nzd=round(gross_margin, 2),
                    estimated_margin_pct=round(margin_pct, 2),
                    landed_cost_nzd=landed["landed"],
                    gst_estimate_nzd=landed["gst"],
                    levy_estimate_nzd=landed["levy"],
                    payment_fee_nzd=landed["payment_fee"],
                    return_allowance_nzd=landed["return_allowance"],
                    demand_score=round(demand.momentum_score, 2),
                    competition_score=round(market.competition_score, 2),
                    risk_score=round(risk_score, 2),
                    social_score=round(social.engagement_score, 2),
                    final_opportunity_score=final_score,
                    ai_recommendation="Strong candidate" if final_score >= 70 else "Review manually",
                    raw_signals={"demand": demand.__dict__, "social": social.__dict__, "market": market.__dict__},
                )
                db.add(record)
                opportunities.append(record)

        db.commit()
        for item in opportunities:
            db.refresh(item)
        return sorted(opportunities, key=lambda x: x.final_opportunity_score, reverse=True)[:max_products]
