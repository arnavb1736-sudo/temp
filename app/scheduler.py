import threading

from apscheduler.schedulers.background import BackgroundScheduler

from app.config import Config
from app.jobs.generate_drafts import GenerateDraftsJob
from app.jobs.publish_posts import PublishPostsJob

scheduler = BackgroundScheduler()

generate_lock = threading.Lock()
publish_lock = threading.Lock()


def generate_job():

    if not generate_lock.acquire(blocking=False):
        print("Generate job already running.")
        return

    try:
        if Config.ENABLE_AUTO_GENERATION:
            print("Running draft generation...")
            GenerateDraftsJob().run()
    finally:
        generate_lock.release()


def publish_job():

    if not publish_lock.acquire(blocking=False):
        print("Publish job already running.")
        return

    try:
        if Config.ENABLE_AUTO_PUBLISH:
            print("Running publish job...")
            PublishPostsJob().run()
    finally:
        publish_lock.release()


def start_scheduler():

    scheduler.add_job(
        generate_job,
        trigger="interval",
        minutes=Config.DRAFT_CHECK_INTERVAL,
        id="generate_drafts",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.add_job(
        publish_job,
        trigger="interval",
        minutes=Config.PUBLISH_CHECK_INTERVAL,
        id="publish_posts",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    print("=" * 50)
    print("Elevastra Scheduler Started")
    print(f"Draft interval   : {Config.DRAFT_CHECK_INTERVAL} minute(s)")
    print(f"Publish interval : {Config.PUBLISH_CHECK_INTERVAL} minute(s)")
    print(f"Auto Generate    : {Config.ENABLE_AUTO_GENERATION}")
    print(f"Auto Publish     : {Config.ENABLE_AUTO_PUBLISH}")
    print("=" * 50)