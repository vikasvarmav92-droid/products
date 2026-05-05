from celery import Celery

from app.core.config import settings

celery_app = Celery("scanner", broker=settings.redis_url)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(86400.0, daily_scan.s(), name="run daily scans")


@celery_app.task
def daily_scan():
    # Placeholder for pulling saved user keywords and triggering scans.
    return "Daily scan triggered"
