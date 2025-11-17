#!/usr/bin/env python3
"""
Auto updater utility runs a callback periodically on a daemon thread.
"""

import threading
import time


class AutoUpdater:
    def __init__(self, interval_seconds, callback):
        self.interval = interval_seconds
        self.callback = callback
        self._running = False
        self._thread = None

    def _worker(self):
        while self._running:
            try:
                self.callback()
            except Exception:
                pass
            time.sleep(self.interval)

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
