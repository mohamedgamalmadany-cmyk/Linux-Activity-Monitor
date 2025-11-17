#!/usr/bin/env python3
"""
GUI Activity Log
The bottom log panel only
"""

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
from config import LIGHT, DARK


def create_activity_log(parent):
    """Create the activity log panel"""
    log_frame = tk.Frame(parent, bg=LIGHT)
    log_frame.pack(fill='x', padx=20, pady=(0, 20))
    
    tk.Label(
        log_frame,
        text="📝 Activity Log",
        font=('Arial', 12, 'bold'),
        bg=LIGHT
    ).pack(anchor='w', pady=(0, 5))
    
    log_text = scrolledtext.ScrolledText(
        log_frame,
        height=6,
        font=('Courier', 9),
        bg='#ecf0f1',
        fg=DARK
    )
    # Allow the log area to expand vertically so scrolling behaves naturally
    log_text.pack(fill='both', expand=True)
    
    return log_text


def add_log_message(log_widget, message):
    """Add a message to log"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_widget.insert('end', f"[{timestamp}] {message}\n")
    log_widget.see('end')
