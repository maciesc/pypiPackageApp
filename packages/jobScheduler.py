from apscheduler.schedulers.background import BackgroundScheduler
from packages.jobs import download_and_index_packages


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(download_and_index_packages, 'cron', hour=0, minute=0, timezone="utc")
    scheduler.start()
