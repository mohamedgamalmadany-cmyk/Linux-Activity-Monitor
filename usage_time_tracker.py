#!/usr/bin/env python3
"""
Track active and idle time for the user session.
Simple implementation: record activity timestamps on GUI events.
"""

import time
from datetime import datetime, timedelta


class UsageTimeTracker:
    def __init__(self, idle_threshold_minutes=5):
        self.start_time = datetime.now()
        self.last_activity = datetime.now()
        self.idle_threshold = timedelta(minutes=idle_threshold_minutes)
        self.total_idle = timedelta(0)
        self._last_idle_start = None

    def start(self):
        self.start_time = datetime.now()
        self.last_activity = datetime.now()

    def record_activity(self):
        now = datetime.now()
        # if we were idle, accumulate idle time
        if self._last_idle_start:
            self.total_idle += (now - self._last_idle_start)
            self._last_idle_start = None
        self.last_activity = now

    def update_idle_state(self):
        now = datetime.now()
        if (now - self.last_activity) >= self.idle_threshold:
            if not self._last_idle_start:
                self._last_idle_start = self.last_activity + self.idle_threshold

    def get_active_time(self):
        now = datetime.now()
        elapsed = now - self.start_time
        active = elapsed - self.total_idle
        return active

    def get_idle_time(self):
        now = datetime.now()
        if self._last_idle_start:
            return now - self._last_idle_start
        return timedelta(0)

    def is_idle(self):
        return (datetime.now() - self.last_activity) >= self.idle_threshold
