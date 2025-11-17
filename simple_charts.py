#!/usr/bin/env python3
"""
Simple chart utilities using matplotlib.
Each function returns a matplotlib Figure object ready to embed.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def bar_top_commands(commands):
    """commands: list of (label, count). Returns horizontal bar Figure."""
    labels = [c for c, _ in commands]
    counts = [n for _, n in commands]
    fig, ax = plt.subplots(figsize=(6, 3))
    y_pos = range(len(labels))[::-1]
    ax.barh(y_pos, counts, color='#3498db')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Count')
    plt.tight_layout()
    return fig


def line_hourly_activity(hours, counts):
    """hours: list of hour labels; counts: list of values. Returns line Figure."""
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(hours, counts, marker='o', color='#2ecc71')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Events')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def pie_file_types(ext_counts):
    """ext_counts: list of (ext, count). Returns pie Figure (max 6 slices)."""
    MAX = 6
    labels = [e for e, _ in ext_counts]
    sizes = [n for _, n in ext_counts]
    if len(labels) > MAX:
        others = sum(sizes[MAX-1:])
        labels = labels[:MAX-1] + ['other']
        sizes = sizes[:MAX-1] + [others]
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.tight_layout()
    return fig
