from app.providers.base.interfaces import DemandSignal, TrendsProvider


class GoogleTrendsProvider(TrendsProvider):
    """Placeholder connector. Integrate pytrends or an API-backed trends source here."""

    def get_demand(self, keyword: str) -> DemandSignal:
        raise NotImplementedError("Google Trends provider not yet configured.")
