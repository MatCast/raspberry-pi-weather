import schedule
from firestore_scheduler import run_continuously, scheduled_write

scheduled_write()
schedule.run_all()
stop_run_continuously = run_continuously(1)
