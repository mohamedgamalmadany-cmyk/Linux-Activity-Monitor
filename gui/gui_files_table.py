#!/usr/bin/env python3
"""
GUI Files Table
The files table (shows most accessed files)
"""

import tkinter as tk
from tkinter import ttk
from config import LIGHT


def create_files_table(parent):
    """Create the files table"""
    files_frame = tk.Frame(parent, bg=LIGHT)
    # Keep the files table compact so it doesn't force a large window
    files_frame.pack(fill='x', padx=20, pady=10)
    
    tk.Label(
        files_frame,
        text="📁 Top 5 Most Accessed Files",
        font=('Arial', 14, 'bold'),
        bg=LIGHT
    ).pack(anchor='w', pady=(0, 10))
    
    tree = ttk.Treeview(
        files_frame,
        columns=('File', 'Count'),
        show='headings',
        height=6
    )
    tree.heading('File', text='File Path')
    tree.heading('Count', text='Count')
    tree.column('File', width=600)
    tree.column('Count', width=100)
    tree.pack(fill='x')
    
    return tree
