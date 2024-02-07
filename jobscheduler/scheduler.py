from jobscheduler.recommendations import executeRecommendations
from jobscheduler.recommendations import executeRecommendations
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from time import sleep
import apscheduler.schedulers.background


def start():
    scheduler = BackgroundScheduler()

    # Configure the job trigger (e.g., every 5 minutes)
    cron_trigger = CronTrigger(minute='*/1')
    scheduler.add_job(executeRecommendations, cron_trigger, id="recommendations")
    scheduler.start()
    try:
        while True:
            sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        pass
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    start()
"""def start():
    scheduler.start()
    cronTrigger = CronTrigger(minute='*/2')
    scheduler.add_job(executeRecommendations, cronTrigger, id="recommendations")

if __name__ == "__main__":
    start()
    try:
        while True:
            pass
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        scheduler.shutdown()"""

"""def start():
    scheduler.start()
    two_minutes_from_now = datetime.now() + timedelta(minutes=2)

    # Configure CronTrigger to run once, 2 minutes from now
    cronTrigger = CronTrigger(
        year=two_minutes_from_now.year,
        month=two_minutes_from_now.month,
        day=two_minutes_from_now.day,
        hour=two_minutes_from_now.hour,
        minute=two_minutes_from_now.minute,
        second=0,
    )

    scheduler.add_job(executeRecommendations, cronTrigger, id="recommendations")

if __name__ == "__main__":
    start()

 def start():
    scheduler.start()
    cronTrigger = CronTrigger(
        year="*", month="*", day="*", hour="14", minute="07", second="0"
    )  # will run at 8pm each day
    scheduler.add_job(executeRecommendations, cronTrigger, id="recommendations")

    sleep(5)"""
