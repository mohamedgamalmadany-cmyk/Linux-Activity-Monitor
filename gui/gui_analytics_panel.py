#!/usr/bin/env python3
"""
GUI Analytics Panel
Provides a Toplevel analytics window with Notebook tabs for overview, productivity, patterns, and insights.
"""

import tkinter as tk
from tkinter import ttk
from config import LIGHT, BLUE, GREEN, RED


def create_analytics_window(parent, analyzer):
    """Open a new analytics window using the provided DataAnalyzer instance."""
    try:
        top = tk.Toplevel(parent)
        top.title('📊 Analytics')
        top.geometry('800x600')
        top.configure(bg=LIGHT)

        notebook = ttk.Notebook(top)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        report = analyzer.generate_summary_report()

        # Overview tab
        frame_over = tk.Frame(notebook, bg=LIGHT)
        notebook.add(frame_over, text='Overview')

        score = report.get('productivity_score', 0)
        score_label = tk.Label(frame_over, text=f"{score}", font=('Arial', 36, 'bold'), bg=LIGHT, fg=BLUE)
        score_label.pack(pady=10)
        tk.Label(frame_over, text='Productivity Score', font=('Arial', 12), bg=LIGHT).pack()

        # Key metrics grid
        metrics = tk.Frame(frame_over, bg=LIGHT)
        metrics.pack(pady=8)
        wk = report.get('weekly', {})
        items = [
            ('This week', wk.get('this_week', 0)),
            ('Last week', wk.get('last_week', 0)),
            ('Top hours', ', '.join([h for h, _ in report.get('top_hours', [])]) or 'N/A')
        ]
        for i, (k, v) in enumerate(items):
            tk.Label(metrics, text=k+':', font=('Arial', 10, 'bold'), bg=LIGHT).grid(row=i, column=0, sticky='w', padx=6, pady=4)
            tk.Label(metrics, text=str(v), font=('Arial', 10), bg=LIGHT).grid(row=i, column=1, sticky='w', padx=6, pady=4)

        # Productivity tab
        frame_prod = tk.Frame(notebook, bg=LIGHT)
        notebook.add(frame_prod, text='Productivity')
        tk.Label(frame_prod, text='Top productive hours', font=('Arial', 12, 'bold'), bg=LIGHT).pack(anchor='w', padx=8, pady=6)
        for h, c in report.get('top_hours', []):
            tk.Label(frame_prod, text=f"Hour {h}: {c} events", bg=LIGHT).pack(anchor='w', padx=12)

        tk.Label(frame_prod, text='Work sessions', font=('Arial', 12, 'bold'), bg=LIGHT).pack(anchor='w', padx=8, pady=(12, 6))
        for s in report.get('sessions', [])[:10]:
            tk.Label(frame_prod, text=f"{s['start']} → {s['end']} • {s['duration_min']} min ({s['events']} events)", bg=LIGHT).pack(anchor='w', padx=12)

        # Patterns tab
        frame_pat = tk.Frame(notebook, bg=LIGHT)
        notebook.add(frame_pat, text='Patterns')
        tk.Label(frame_pat, text='Top Commands', font=('Arial', 12, 'bold'), bg=LIGHT).pack(anchor='w', padx=8, pady=6)
        for c in report.get('command_patterns', [])[:20]:
            tk.Label(frame_pat, text=f"{c['command']} • {c['count']}", bg=LIGHT, anchor='w').pack(fill='x', padx=12)

        tk.Label(frame_pat, text='File types', font=('Arial', 12, 'bold'), bg=LIGHT).pack(anchor='w', padx=8, pady=(12, 6))
        for e in report.get('file_patterns', {}).get('by_extension', []):
            tk.Label(frame_pat, text=f"{e['ext']}: {e['count']}", bg=LIGHT).pack(anchor='w', padx=12)

        # Insights tab
        frame_ins = tk.Frame(notebook, bg=LIGHT)
        notebook.add(frame_ins, text='Insights')
        tk.Label(frame_ins, text='Smart Recommendations', font=('Arial', 12, 'bold'), bg=LIGHT).pack(anchor='w', padx=8, pady=6)
        for ins in report.get('insights', []):
            tk.Label(frame_ins, text=f"{ins.get('icon','')} {ins.get('message','')}", bg=LIGHT, wraplength=700, justify='left').pack(anchor='w', padx=12, pady=4)

        return top
    except Exception as e:
        # fail gracefully
        tk.messagebox.showerror('Analytics Error', str(e))
        return None
