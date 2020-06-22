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

code_dir_to_monitor = "/app"
# celery_working_dir = code_dir_to_monitor  # happen to be the same. It may be different on your machine
celery_working_dir = os.getcwd()
celery_cmdline = 'celery worker --app crawler -l info -c 1 -E --queues queue_crawler'.split(" ")


class MyHandler(PatternMatchingEventHandler):

    def __init__(self, cmdline, workdir, **keywords):
        super().__init__(**keywords)
        self.cmdline = cmdline
        self.workdir = workdir
        self.current_proc = None

    def run_worker(self):
        cmdline = self.cmdline
        print("Ready to call {} ".format(cmdline))
        os.chdir(celery_working_dir)
        proc = subprocess.Popen(cmdline)
        self.current_proc = psutil.Process(proc.pid)
        print("Done callling {} ".format(cmdline))


    def on_any_event(self, event):
        print("detected change. event = {}".format(event))

        # for proc in psutil.process_iter():
        #     proc_cmdline = self._get_proc_cmdline(proc)
        #     if not proc_cmdline or len(proc_cmdline) < len(celery_cmdline):
        #         continue
        #
        #     is_celery_worker = 'python' in proc_cmdline[0].lower() \
        #                        and celery_cmdline[0] == proc_cmdline[1] \
        #                        and celery_cmdline[1] == proc_cmdline[2]
        #
        #     if not is_celery_worker:
        #         continue
        #
        #     proc.kill()
        #     print("Just killed {} on working dir {}".format(proc_cmdline, proc.cwd()))

        if self.current_proc:
            self.current_proc.kill()

        self.run_worker()
        # run_worker()

    def _get_proc_cmdline(self, proc):
        try:
            return proc.cmdline()
        except Exception as e:
            return []


def run_worker(cmdline):
    print("Ready to call {} ".format(cmdline))
    os.chdir(celery_working_dir)
    subprocess.Popen(cmdline)
    print("Done callling {} ".format(cmdline))


def main():
    # run_worker(celery_cmdline)

    event_handler = MyHandler(celery_cmdline, celery_working_dir, patterns=["*.py"])
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


if __name__ == "__main__":
    main()
