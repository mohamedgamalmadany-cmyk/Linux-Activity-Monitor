#!/usr/bin/env python3
"""
GUI Commands Table
The commands table only
"""

import tkinter as tk
from tkinter import ttk
from config import LIGHT


def create_commands_table(parent):
    """Create the commands table"""
    commands_frame = tk.Frame(parent, bg=LIGHT)
    # Pack without expanding to avoid forcing the whole UI to grow too large
    commands_frame.pack(fill='x', padx=20, pady=10)
    
    tk.Label(
        commands_frame,
        text="🔝 Top 5 Most Used Commands",
        font=('Arial', 14, 'bold'),
        bg=LIGHT
    ).pack(anchor='w', pady=(0, 10))
    
    tree = ttk.Treeview(
        commands_frame,
        columns=('Command', 'Count'),
        show='headings',
        height=6
    )
    tree.heading('Command', text='Command')
    tree.heading('Count', text='Count')
    tree.column('Command', width=600, stretch=True)
    tree.column('Count', width=100, anchor='center')

    # Vertical scrollbar
    v_scroll = ttk.Scrollbar(commands_frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=v_scroll.set)

    # Horizontal scrollbar
    h_scroll = ttk.Scrollbar(commands_frame, orient='horizontal', command=tree.xview)
    tree.configure(xscrollcommand=h_scroll.set)

    # Layout: tree expands, v_scroll on right, h_scroll at bottom
    tree.pack(fill='x')
    v_scroll.pack(fill='y', side='right')
    h_scroll.pack(fill='x', side='bottom')
    
    return tree
