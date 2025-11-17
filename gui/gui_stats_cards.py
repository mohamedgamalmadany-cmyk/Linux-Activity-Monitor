#!/usr/bin/env python3
"""
GUI Statistics Cards
The 4 colored cards (updated to include files)
"""

import tkinter as tk
from config import LIGHT, BLUE, GREEN, RED, TEAL  


def create_stats_cards(parent):
    """Create the 4 statistics cards"""
    stats_frame = tk.Frame(parent, bg=LIGHT)
    stats_frame.pack(fill='x', padx=20, pady=10)
    
    tk.Label(
        stats_frame,
        text="📈 Key Statistics",
        font=('Arial', 14, 'bold'),
        bg=LIGHT
    ).pack(anchor='w', pady=(0, 10))
    
    cards_frame = tk.Frame(stats_frame, bg=LIGHT)
    cards_frame.pack(fill='x')
    
    # Card 1: Total Events
    total_events_var = tk.StringVar(value="0")
    create_single_card(cards_frame, "🔢 Total Events", total_events_var, BLUE, 0)
    
    # Card 2: Commands
    total_commands_var = tk.StringVar(value="0")
    create_single_card(cards_frame, "⌨️ Commands", total_commands_var, GREEN, 1)
    
    # Card 3: Processes
    total_processes_var = tk.StringVar(value="0")
    create_single_card(cards_frame, "⚙️ Processes", total_processes_var, RED, 2)
    
    # Card 4: Files 
    total_files_var = tk.StringVar(value="0")
    create_single_card(cards_frame, "📁 Files", total_files_var, TEAL, 3)
    
    return {
        'events_var': total_events_var,
        'commands_var': total_commands_var,
        'processes_var': total_processes_var,
        'files_var': total_files_var  # ← جديد
    }


def create_single_card(parent, title, value_var, color, column):
    """Create one card"""
    card = tk.Frame(parent, bg=color, relief='raised', borderwidth=2)
    card.grid(row=0, column=column, padx=10, pady=5, sticky='ew')
    parent.columnconfigure(column, weight=1)
    
    tk.Label(
        card, text=title, font=('Arial', 11, 'bold'),
        bg=color, fg='white'
    ).pack(pady=(10, 5))
    
    tk.Label(
        card, textvariable=value_var, font=('Arial', 24, 'bold'),
        bg=color, fg='white'
    ).pack(pady=(0, 10))
