#!/usr/bin/env python3
"""
Quick analysis helpers that wrap DataAnalyzer to produce chart-friendly datasets.
"""

from data_analyzer import DataAnalyzer
from collections import defaultdict


def summary_for_charts():
    a = DataAnalyzer()
    report = a.generate_summary_report()

    # top commands -> list of (label, count)
    top_cmds = [(c['command'], c['count']) for c in report.get('command_patterns', [])]

    # hourly activity (last 24 hours)
    # We'll query DataAnalyzer for most productive hours and expand to 24 slots
    hours = [str(h) for h, _ in report.get('top_hours', [])]

    # file types
    ext = [(e['ext'], e['count']) for e in report.get('file_patterns', {}).get('by_extension', [])]

    return {'top_commands': top_cmds, 'hours': hours, 'file_types': ext, 'productivity_score': report.get('productivity_score', 0)}
