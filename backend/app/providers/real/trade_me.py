from app.providers.base.interfaces import MarketSignal, MarketplaceProvider


class TradeMeProvider(MarketplaceProvider):
    """Placeholder connector for Trade Me marketplace analytics."""

    def get_market_signal(self, keyword: str) -> MarketSignal:
        raise NotImplementedError("Trade Me provider not yet configured.")
