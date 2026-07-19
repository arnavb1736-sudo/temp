import threading
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.config import Config
from app.jobs.generate_drafts import GenerateDraftsJob
from app.jobs.publish_posts import PublishPostsJob

scheduler = BackgroundScheduler()

generate_lock = threading.Lock()
publish_lock = threading.Lock()


def log(message):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")


def generate_job():

    log("Generate scheduler triggered.")

    if not generate_lock.acquire(blocking=False):
        log("Generate job already running.")
        return

    try:
        if Config.ENABLE_AUTO_GENERATION:
            GenerateDraftsJob().run()
    except Exception as e:
        log(f"Generate job crashed: {e}")
    finally:
        generate_lock.release()


def publish_job():

    log("Publish scheduler triggered.")

    if not publish_lock.acquire(blocking=False):
        log("Publish job already running.")
        return

    try:
        if Config.ENABLE_AUTO_PUBLISH:
            PublishPostsJob().run()
    except Exception as e:
        log(f"Publish job crashed: {e}")
    finally:
        publish_lock.release()


def start_scheduler():

    scheduler.add_job(
        generate_job,
        "interval",
        minutes=Config.DRAFT_CHECK_INTERVAL,
        id="generate_drafts",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        publish_job,
        "interval",
        minutes=Config.PUBLISH_CHECK_INTERVAL,
        id="publish_posts",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    log("=" * 50)
    log("Elevastra Scheduler Started")
    log(f"Draft interval: {Config.DRAFT_CHECK_INTERVAL}")
    log(f"Publish interval: {Config.PUBLISH_CHECK_INTERVAL}")
    log(f"Auto Generate: {Config.ENABLE_AUTO_GENERATION}")
    log(f"Auto Publish: {Config.ENABLE_AUTO_PUBLISH}")
    log("=" * 50)