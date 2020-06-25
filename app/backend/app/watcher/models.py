import asyncio
import logging
import os
from pathlib import Path

logger = logging.getLogger("FileChangeDetector.error")

class FileChangeDetector:
    def __init__(self, *reload_dirs):
        self.mtimes = {}
        self.reload_dirs = reload_dirs
        self.callback = lambda display_path:logger.warning("Detected file change in '%s'", display_path)

    def set_callback(self, callback):
        if callback is None:
            self.callback = lambda display_path: None
        else:
            self.callback = callback

    async def get_coroutine(self, interval = 1, run_until_file_changed = False):
        while True:
            await asyncio.sleep(interval)
            is_file_changed = self()
            if is_file_changed and run_until_file_changed:
                break

    def __call__(self):
        for filename in self.iter_py_files():
            try:
                mtime = os.path.getmtime(filename)
            except OSError:  # pragma: nocover
                continue

            old_time = self.mtimes.get(filename)
            if old_time is None:
                self.mtimes[filename] = mtime
                continue
            elif mtime > old_time:
                display_path = os.path.normpath(filename)
                if Path.cwd() in Path(filename).parents:
                    display_path = os.path.normpath(os.path.relpath(filename))
                message = "Detected file change in '%s'"
                logger.warning(message, display_path)
                self.callback()
                return True
        return False

    def iter_py_files(self):
        for reload_dir in self.reload_dirs:
            for subdir, dirs, files in os.walk(reload_dir):
                for file in files:
                    if file.endswith(".py"):
                        yield subdir + os.sep + file