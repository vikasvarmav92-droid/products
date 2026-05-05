from dataclasses import dataclass


@dataclass
class DemandSignal:
    growth_pct: float
    momentum_score: float


@dataclass
class SocialSignal:
    growth_pct: float
    engagement_score: float


@dataclass
class MarketSignal:
    listing_count: int
    avg_price_nzd: float
    competition_score: float


@dataclass
class SupplierSignal:
    product_name: str
    image_url: str
    supplier_url: str
    product_cost_nzd: float
    shipping_cost_nzd: float
    shipping_days: int
    supplier_rating: float


class TrendsProvider:
    def get_demand(self, keyword: str) -> DemandSignal:
        raise NotImplementedError


class SocialProvider:
    def get_social_signal(self, keyword: str) -> SocialSignal:
        raise NotImplementedError


class MarketplaceProvider:
    def get_market_signal(self, keyword: str) -> MarketSignal:
        raise NotImplementedError


class SupplierProvider:
    def search_products(self, keyword: str, limit: int) -> list[SupplierSignal]:
        raise NotImplementedError
