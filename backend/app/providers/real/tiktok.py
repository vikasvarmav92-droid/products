from app.providers.base.interfaces import SocialProvider, SocialSignal


class TikTokCreativeCenterProvider(SocialProvider):
    """Placeholder connector for TikTok Creative Center data."""

    def get_social_signal(self, keyword: str) -> SocialSignal:
        raise NotImplementedError("TikTok provider not yet configured.")
