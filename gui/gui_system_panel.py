#!/usr/bin/env python3
"""
GUI System Resources Panel
Displays CPU, RAM, Disk and Network I/O using progress bars and updates in background.
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
from config import LIGHT, DARK
import system_resources_monitor as srm


def create_system_panel(parent, update_interval_ms=2000, disk_path='/'):
    """Create and start a system resources panel.

    Returns a dict with keys:
      - 'frame': the container frame
      - 'stop': callable to stop background updates
    """
    panel = tk.Frame(parent, bg=LIGHT)
    panel.pack(fill='x', padx=20, pady=6)

    header = tk.Label(panel, text="🔥 System Resources", font=('Arial', 11, 'bold'), bg=LIGHT)
    header.grid(row=0, column=0, columnspan=3, sticky='w', pady=(0, 4))

    # Make a compact style for progressbars
    style = ttk.Style()
    style.theme_use('default')
    # configure the default horizontal progressbar to be a bit thicker
    style.configure('Horizontal.TProgressbar', troughcolor=LIGHT, thickness=10)

    # helper to build rows using grid for tighter layout
    def make_row(row_idx, title_text):
        title = tk.Label(panel, text=title_text, font=('Arial', 9, 'bold'), bg=LIGHT)
        title.grid(row=row_idx, column=0, sticky='w')

        bar = ttk.Progressbar(panel, style='Horizontal.TProgressbar', orient='horizontal', mode='determinate')
        bar.grid(row=row_idx, column=1, sticky='we', padx=8)

        value = tk.Label(panel, text='--', font=('Arial', 9), bg=LIGHT)
        value.grid(row=row_idx, column=2, sticky='e')

        return {'title': title, 'value': value, 'bar': bar}

    # make 4 compact rows
    cpu_row = make_row(1, '🔥 CPU')
    ram_row = make_row(2, '🧠 RAM')
    disk_row = make_row(3, '💾 Disk')
    net_row = make_row(4, '📡 Network')

    # allow the middle column (bars) to expand
    panel.grid_columnconfigure(1, weight=1)

    running = True

    def update_ui(data):
        try:
            cpu_pct = data.get('cpu', {}).get('percent', 0)
            cpu_row['bar']['value'] = cpu_pct
            cpu_row['value'].config(text=f"{cpu_pct}%")

            mem = data.get('memory', {})
            mem_pct = mem.get('percent', 0)
            mem_row['bar']['value'] = mem_pct
            mem_row['value'].config(text=f"{mem_pct}% ({mem.get('used_gb',0)}/{mem.get('total_gb',0)} GB)")

            disk = data.get('disk', {})
            disk_pct = disk.get('percent', 0)
            disk_row['bar']['value'] = disk_pct
            disk_row['value'].config(text=f"{disk_pct}% ({disk.get('used_gb',0)}/{disk.get('total_gb',0)} GB)")

            net = data.get('network', {})
            sent = net.get('sent_mb', 0)
            recv = net.get('recv_mb', 0)
            net_row['value'].config(text=f"Sent: {sent} MB / Recv: {recv} MB")
        except Exception:
            # swallow UI update errors
            pass

    def update_ui(data):
        try:
            # handle case where monitor returned an error
            if not data or 'error' in data:
                cpu_row['bar'].configure(value=0)
                ram_row['bar'].configure(value=0)
                disk_row['bar'].configure(value=0)
                net_row['value'].config(text='N/A')
                return

            cpu_pct = data.get('cpu', {}).get('percent', 0) or 0
            cpu_row['bar'].configure(value=cpu_pct)
            cpu_row['value'].config(text=f"{cpu_pct}%")

            mem = data.get('memory', {})
            mem_pct = mem.get('percent', 0) or 0
            # fallback: compute percent if missing
            if mem_pct == 0 and mem.get('total'):
                try:
                    mem_pct = round((mem.get('used', 0) / max(1, mem.get('total'))) * 100, 1)
                except Exception:
                    mem_pct = 0
            ram_row['bar'].configure(value=mem_pct)
            ram_row['value'].config(text=f"{mem_pct}% ({mem.get('used_gb',0)}/{mem.get('total_gb',0)} GB)")

            disk = data.get('disk', {})
            disk_pct = disk.get('percent', 0) or 0
            disk_row['bar'].configure(value=disk_pct)
            disk_row['value'].config(text=f"{disk_pct}% ({disk.get('used_gb',0)}/{disk.get('total_gb',0)} GB)")

            net = data.get('network', {})
            sent = net.get('sent_mb', 0)
            recv = net.get('recv_mb', 0)
            net_row['value'].config(text=f"Sent: {sent} MB / Recv: {recv} MB")
        except Exception:
            # swallow UI update errors
            pass

    # Background worker that polls psutil and updates the UI
    def worker():
        while running:
            try:
                data = srm.get_all(disk_path)
                # schedule UI update on main thread
                parent.after(0, lambda d=data: update_ui(d))
            except Exception:
                # ignore errors from psutil or UI scheduling
                pass
            time.sleep(update_interval_ms / 1000.0)

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    def stop():
        nonlocal running
        running = False

    return {'frame': panel, 'stop': stop}
