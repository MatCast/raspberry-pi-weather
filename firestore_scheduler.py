import threading
import time

import schedule
# from temperature_bmp import read_all
from firestore_temperature import add_temperature_reading
import datetime


def run_continuously(interval=2, func=None, *args, **kwargs):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)
                if func:
                    func(args, kwargs)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def read_temp_and_write():
    # data = read_all()
    data = {
        "humidity": 58.09,
        "pressure": 962.76,
        "temperature": 16.03,
        "timestamp": datetime.datetime.utcnow()
    }
    add_temperature_reading(data)


def scheduled_write():
    schedule.every(10).seconds.do(read_temp_and_write)

