import random

from app.providers.base.interfaces import (
    DemandSignal,
    MarketSignal,
    MarketplaceProvider,
    SocialSignal,
    SocialProvider,
    SupplierProvider,
    SupplierSignal,
    TrendsProvider,
)


class MockTrendsProvider(TrendsProvider):
    def get_demand(self, keyword: str) -> DemandSignal:
        return DemandSignal(growth_pct=random.uniform(3, 70), momentum_score=random.uniform(20, 100))


class MockSocialProvider(SocialProvider):
    def get_social_signal(self, keyword: str) -> SocialSignal:
        return SocialSignal(growth_pct=random.uniform(-10, 90), engagement_score=random.uniform(10, 100))


class MockMarketplaceProvider(MarketplaceProvider):
    def get_market_signal(self, keyword: str) -> MarketSignal:
        listing_count = random.randint(5, 300)
        competition_score = max(0.0, 100 - listing_count / 3)
        return MarketSignal(
            listing_count=listing_count,
            avg_price_nzd=random.uniform(25, 250),
            competition_score=competition_score,
        )


class MockSupplierProvider(SupplierProvider):
    def search_products(self, keyword: str, limit: int) -> list[SupplierSignal]:
        products = []
        for idx in range(limit):
            products.append(
                SupplierSignal(
                    product_name=f"{keyword.title()} Variant {idx + 1}",
                    image_url="https://placehold.co/300x300",
                    supplier_url=f"https://example-supplier.com/{keyword}-{idx + 1}",
                    product_cost_nzd=random.uniform(5, 70),
                    shipping_cost_nzd=random.uniform(2, 20),
                    shipping_days=random.randint(5, 35),
                    supplier_rating=random.uniform(3.5, 5),
                )
            )
        return products
