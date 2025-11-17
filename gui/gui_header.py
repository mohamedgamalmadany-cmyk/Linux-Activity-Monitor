#!/usr/bin/env python3
"""
GUI Header Component
Top blue header only
"""

import tkinter as tk
from config import DARK


def create_header(parent):
    """Create the top header and return frame plus status labels."""
    header_frame = tk.Frame(parent, bg=DARK, height=80)
    header_frame.pack(fill='x', pady=(0, 10))

    title = tk.Label(
        header_frame,
        text="📊 Linux Activity Monitor",
        font=('Arial', 20, 'bold'),
        bg=DARK,
        fg='white'
    )
    title.pack(pady=(10, 6))

    # status row
    status_frame = tk.Frame(header_frame, bg=DARK)
    status_frame.pack(fill='x', pady=(0, 8))

    last_update_lbl = tk.Label(status_frame, text='Last Update: --', font=('Arial', 10), bg=DARK, fg='white')
    last_update_lbl.pack(side='left', padx=12)

    active_time_lbl = tk.Label(status_frame, text='⏱️ Active Time: 0m', font=('Arial', 10), bg=DARK, fg='white')
    active_time_lbl.pack(side='left', padx=12)

    return header_frame, {'last_update': last_update_lbl, 'active_time': active_time_lbl}
