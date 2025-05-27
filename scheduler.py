from apscheduler.schedulers.background import BackgroundScheduler
from follow_up import check_for_pending_requests

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=check_for_pending_requests, trigger="interval", hours=1)  # every 1 hour
    scheduler.start()
    print("[SCHEDULER] Follow-up checker started.")
