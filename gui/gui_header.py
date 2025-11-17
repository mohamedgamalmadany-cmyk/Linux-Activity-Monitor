#!/usr/bin/env python3
"""
GUI Header Component
Top blue header only
"""

import tkinter as tk
from config import DARK


def create_header(parent):
    """Create the top header"""
    header_frame = tk.Frame(parent, bg=DARK, height=80)
    header_frame.pack(fill='x', pady=(0, 10))
    
    title = tk.Label(
        header_frame,
        text="📊 Linux Activity Monitor",
        font=('Arial', 20, 'bold'),
        bg=DARK,
        fg='white'
    )
    title.pack(pady=20)
    
    return header_frame
