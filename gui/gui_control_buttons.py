#!/usr/bin/env python3
"""
GUI Control Buttons
The 4 control buttons only
"""

import tkinter as tk
from config import LIGHT, BLUE, GREEN, ORANGE, PURPLE


def create_control_buttons(parent, collect_callback, refresh_callback, auto_callback, export_callback, analytics_callback=None):
    """Create the control buttons. Optional `analytics_callback` opens analytics window."""
    control_frame = tk.Frame(parent, bg=LIGHT)
    control_frame.pack(fill='x', padx=20, pady=10)
    
    btn_style = {'font': ('Arial', 11, 'bold'), 'width': 15, 'height': 2}
    
    # Button 1: Collect
    tk.Button(
        control_frame,
        text="🔄 Collect Data",
        bg=BLUE,
        fg='white',
        command=collect_callback,
        **btn_style
    ).pack(side='left', padx=5)
    
    # Button 2: Refresh
    refresh_btn = tk.Button(
        control_frame,
        text="♻️ Refresh View",
        bg=GREEN,
        fg='white',
        command=refresh_callback,
        **btn_style
    )
    refresh_btn.pack(side='left', padx=5)
    
    # Button 3: Auto
    auto_btn = tk.Button(
        control_frame,
        text="▶️ Start Auto",
        bg=ORANGE,
        fg='white',
        command=auto_callback,
        **btn_style
    )
    auto_btn.pack(side='left', padx=5)
    
    # Button 4: Export
    tk.Button(
        control_frame,
        text="📤 Export CSV",
        bg=PURPLE,
        fg='white',
        command=export_callback,
        **btn_style
    ).pack(side='left', padx=5)

    analytics_btn = None
    if analytics_callback:
        analytics_btn = tk.Button(
            control_frame,
            text="📊 Analytics",
            bg=BLUE,
            fg='white',
            command=analytics_callback,
            **btn_style
        )
        analytics_btn.pack(side='left', padx=5)
    
    # Return auto, refresh, and analytics button (analytics may be None)
    return auto_btn, refresh_btn, analytics_btn
