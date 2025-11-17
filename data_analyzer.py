#!/usr/bin/env python3
"""
Data Analyzer
Provides analytics functions for the activity monitor using the existing SQLite database.
"""

import sqlite3
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from config import DB_FILE


class DataAnalyzer:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_FILE

    def _fetch(self, query, params=()):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()
            conn.close()
            return rows
        except Exception:
            return []

    def get_productivity_score(self, days=7):
        """Return an integer score 0-100 based on activity count and active hours."""
        try:
            end = datetime.now()
            start = end - timedelta(days=days)
            q = 'SELECT COUNT(*) FROM activity_log WHERE timestamp >= ?'
            total = self._fetch(q, (start.strftime('%Y-%m-%d %H:%M:%S'),))
            total_events = total[0][0] if total else 0

            # count distinct active hours
            q2 = "SELECT DISTINCT strftime('%Y-%m-%d %H', timestamp) as hr FROM activity_log WHERE timestamp >= ?"
            hours = self._fetch(q2, (start.strftime('%Y-%m-%d %H:%M:%S'),))
            active_hours = len(hours)

            # heuristics: expected 8 active hours/day, 20 events/day
            event_density = min(1.0, total_events / (days * 20))
            continuity = min(1.0, active_hours / (days * 8))

            score = int(100 * (0.6 * event_density + 0.4 * continuity))
            return max(0, min(100, score))
        except Exception:
            return 0

    def get_most_productive_hours(self, days=7, top_n=3):
        """Return top N hours (HH) with highest activity in the given window."""
        try:
            start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
            q = "SELECT strftime('%H', timestamp) AS hour, COUNT(*) FROM activity_log WHERE timestamp >= ? GROUP BY hour ORDER BY COUNT(*) DESC LIMIT ?"
            rows = self._fetch(q, (start, top_n))
            return [(r[0], r[1]) for r in rows]
        except Exception:
            return []

    def get_command_patterns(self, top_n=10):
        """Return top commands and their counts."""
        try:
            q = "SELECT details, COUNT(*) FROM activity_log WHERE event_type='bash_command' GROUP BY details ORDER BY COUNT(*) DESC LIMIT ?"
            rows = self._fetch(q, (top_n,))
            return [{'command': r[0], 'count': r[1]} for r in rows]
        except Exception:
            return []

    def get_file_activity_patterns(self, top_n=10):
        """Return top file paths and breakdown by extension."""
        try:
            q = "SELECT details, COUNT(*) FROM activity_log WHERE event_type='file_access' GROUP BY details ORDER BY COUNT(*) DESC LIMIT ?"
            rows = self._fetch(q, (top_n,))
            files = [{'path': r[0], 'count': r[1], 'ext': (r[0].split('.')[-1] if '.' in r[0] else '')} for r in rows]

            # extension aggregation
            ext_counter = Counter([f['ext'] or 'unknown' for f in files])
            ext_breakdown = [{'ext': k, 'count': v} for k, v in ext_counter.most_common()]

            return {'top_files': files, 'by_extension': ext_breakdown}
        except Exception:
            return {'top_files': [], 'by_extension': []}

    def get_weekly_comparison(self):
        """Compare this week vs last week total events."""
        try:
            now = datetime.now()
            # start of this week (Monday)
            start_this = now - timedelta(days=now.weekday())
            start_last = start_this - timedelta(days=7)
            end_last = start_this - timedelta(seconds=1)

            q = 'SELECT COUNT(*) FROM activity_log WHERE timestamp BETWEEN ? AND ?'
            this_week = self._fetch(q, (start_this.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%d %H:%M:%S')))
            last_week = self._fetch(q, (start_last.strftime('%Y-%m-%d %H:%M:%S'), end_last.strftime('%Y-%m-%d %H:%M:%S')))
            tw = this_week[0][0] if this_week else 0
            lw = last_week[0][0] if last_week else 0
            change = None
            if lw == 0:
                change = None
            else:
                change = round(((tw - lw) / max(1, lw)) * 100, 1)
            return {'this_week': tw, 'last_week': lw, 'change_percent': change}
        except Exception:
            return {'this_week': 0, 'last_week': 0, 'change_percent': None}

    def get_work_sessions(self, gap_minutes=30):
        """Detect continuous work sessions where gaps between events <= gap_minutes.

        Returns list of sessions with start, end, duration_minutes, event_count.
        """
        try:
            q = 'SELECT timestamp FROM activity_log ORDER BY timestamp ASC'
            rows = self._fetch(q)
            times = [datetime.strptime(r[0], '%Y-%m-%d %H:%M:%S') for r in rows if r and r[0]]
            if not times:
                return []

            sessions = []
            cur_start = times[0]
            cur_end = times[0]
            count = 1
            for t in times[1:]:
                if (t - cur_end).total_seconds() <= gap_minutes * 60:
                    cur_end = t
                    count += 1
                else:
                    duration = (cur_end - cur_start).total_seconds() / 60.0
                    sessions.append({'start': cur_start.strftime('%Y-%m-%d %H:%M:%S'), 'end': cur_end.strftime('%Y-%m-%d %H:%M:%S'), 'duration_min': round(duration, 1), 'events': count})
                    cur_start = t
                    cur_end = t
                    count = 1

            # finalize
            duration = (cur_end - cur_start).total_seconds() / 60.0
            sessions.append({'start': cur_start.strftime('%Y-%m-%d %H:%M:%S'), 'end': cur_end.strftime('%Y-%m-%d %H:%M:%S'), 'duration_min': round(duration, 1), 'events': count})
            return sessions
        except Exception:
            return []

    def get_insights(self):
        """Generate simple actionable insights based on analytics."""
        try:
            score = self.get_productivity_score()
            insights = []
            if score < 40:
                insights.append({'icon': '⚠️', 'type': 'Focus', 'message': 'Low activity — consider scheduling focused work blocks and reducing distractions.'})
            elif score < 70:
                insights.append({'icon': '💡', 'type': 'Improve', 'message': 'Moderate activity — try breaking tasks into 25-50 minute sessions.'})
            else:
                insights.append({'icon': '🎯', 'type': 'Great', 'message': 'High productivity — keep a similar cadence and take regular short breaks.'})

            sessions = self.get_work_sessions()
            long_sessions = [s for s in sessions if s['duration_min'] >= 120]
            if long_sessions:
                insights.append({'icon': '⏰', 'type': 'Break', 'message': 'Detected long sessions — remember to take longer breaks to avoid burnout.'})

            top_hours = self.get_most_productive_hours()
            if top_hours:
                hours = ', '.join([h for h, _ in top_hours])
                insights.append({'icon': '📈', 'type': 'Timing', 'message': f'You are most active around hours: {hours}.'})

            return insights
        except Exception:
            return []

    def generate_summary_report(self):
        """Return a dictionary with all analysis results."""
        return {
            'productivity_score': self.get_productivity_score(),
            'top_hours': self.get_most_productive_hours(),
            'command_patterns': self.get_command_patterns(),
            'file_patterns': self.get_file_activity_patterns(),
            'weekly': self.get_weekly_comparison(),
            'sessions': self.get_work_sessions(),
            'insights': self.get_insights()
        }
