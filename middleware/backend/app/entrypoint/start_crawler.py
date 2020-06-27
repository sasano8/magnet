"""
A python script which starts celery worker and auto reload it when any code change happens.
I did this because Celery worker's "--autoreload" option seems not working for a lot of people.
"""

import time
from watchdog.observers import Observer  ##pip install watchdog
from watchdog.events import PatternMatchingEventHandler
import psutil  ##pip install psutil
import os
import subprocess
import threading



class MyHandler(PatternMatchingEventHandler):

    def __init__(self, cmdline, workdir, **keywords):
        super().__init__(**keywords)

        self.workdir = workdir
        self.current_proc = None

        self.cmdline = None
        self.current_thred = None

        self.cmdline = cmdline

    def run_worker(self):
        cmdline = self.cmdline
        print("Ready to call {} ".format(cmdline))
        os.chdir(self.workdir)
        proc = subprocess.Popen(cmdline)
        self.current_proc = psutil.Process(proc.pid)
        print("Done callling {} ".format(cmdline))
        



    def on_any_event(self, event):
        print("detected change. event = {}".format(event))

        if self.current_proc:
            self.current_proc.terminate()

        self.run_worker()
    ##



def run(code_dir_to_monitor, celery_cmdline, celery_working_dir):

    celery_cmdline = celery_cmdline.split(" ")
    event_handler = MyHandler(celery_cmdline, celery_working_dir, patterns=["*.py"])
    event_handler.on_any_event(None)

    observer = Observer()
    observer.schedule(event_handler, code_dir_to_monitor, recursive=True)
    observer.start()
    print("file change observer started")


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


