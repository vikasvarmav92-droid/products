from app.providers.base.interfaces import SupplierProvider, SupplierSignal


class AliExpressProvider(SupplierProvider):
    """Placeholder connector for AliExpress product search."""

    def search_products(self, keyword: str, limit: int) -> list[SupplierSignal]:
        raise NotImplementedError("AliExpress provider not yet configured.")
