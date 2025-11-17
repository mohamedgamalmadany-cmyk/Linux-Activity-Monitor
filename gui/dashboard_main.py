#!/usr/bin/env python3
"""
Dashboard Main
Combines all GUI components together
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time
from datetime import datetime

import database.database_operations as db
import collectors_mainpulations.bash_history_collector as bash_collector
import collectors_mainpulations.process_collector as proc_collector
import collectors_mainpulations.user_collector as user_collector
import collectors_mainpulations.file_collector as file_collector
import statistics_export.statistics_calculator as stats
import statistics_export.csv_exporter as exporter

from gui import (
    gui_header,
    gui_stats_cards,
    gui_commands_table,
    gui_control_buttons,
    gui_activity_log,
    gui_files_table,
    gui_system_panel,
    gui_analytics_panel
)
from data_analyzer import DataAnalyzer

from config import *


class Dashboard:
    """Main Dashboard that combines everything"""
    
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=LIGHT)
        
        self.auto_running = False
        
        # Create a scrollable content area so the UI fits smaller screens
        header_frame, header_labels = gui_header.create_header(self.root)
        self.header_labels = header_labels

        # usage tracker
        from usage_time_tracker import UsageTimeTracker
        self.usage_tracker = UsageTimeTracker()
        self.usage_tracker.start()
        # bind global user events to record activity
        self.root.bind_all('<Any-KeyPress>', lambda e: self.usage_tracker.record_activity())
        self.root.bind_all('<Motion>', lambda e: self.usage_tracker.record_activity())

        # Scrollable frame
        container = tk.Frame(self.root)
        container.pack(fill='both', expand=True)
        canvas = tk.Canvas(container, bg=LIGHT, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=LIGHT)

        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Initialize analyzer
        self.analyzer = DataAnalyzer()

        # Create GUI components inside the scrollable frame
        self.stats_vars = gui_stats_cards.create_stats_cards(scrollable_frame)
        # System resources panel (below the stats cards)
        self.system_panel = gui_system_panel.create_system_panel(scrollable_frame)
        self.commands_table = gui_commands_table.create_commands_table(scrollable_frame)
        self.files_table = gui_files_table.create_files_table(scrollable_frame)

        # New items section
        self.new_items_frame = tk.Frame(scrollable_frame, bg=LIGHT)
        self.new_items_frame.pack(fill='x', padx=20, pady=(0, 6))
        tk.Label(self.new_items_frame, text='📁 New This Session', font=('Arial', 12, 'bold'), bg=LIGHT).pack(anchor='w')
        self.new_items_list = tk.Listbox(self.new_items_frame, height=6)
        self.new_items_list.pack(fill='x')
        self.last_scan_time = datetime.now()

        # Receive auto, refresh, analytics buttons
        self.auto_btn, self.refresh_btn, self.analytics_btn = gui_control_buttons.create_control_buttons(
            scrollable_frame,
            self.collect_now,
            self.refresh_view,
            self.toggle_auto,
            self.export_csv,
            self.open_analytics
        )

        self.log = gui_activity_log.create_activity_log(scrollable_frame)
        
        # Initial refresh
        self.refresh_view()
        # start periodic UI active-time updater
        self._update_active_time_ui()
    
    def log_msg(self, msg):
        """Add message to log"""
        gui_activity_log.add_log_message(self.log, msg)
    
    def collect_now(self):
        """Collect data button"""
        self.log_msg("🔄 Collecting data...")
        try:
            bash_collector.collect_and_save(db.save_event, MAX_BASH_COMMANDS)
            proc_collector.collect_and_save(db.save_event, MAX_PROCESSES)
            user_collector.collect_and_save(db.save_event)
            file_collector.collect_and_save(db.save_event, MAX_FILES)  # ← جديد
            
            self.log_msg("✅ Data collected")
            self.refresh_view()
            messagebox.showinfo("Success", "Data collected!")
        except Exception as e:
            self.log_msg(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))
    
    def refresh_view(self):
        """Refresh display"""
        self.log_msg("♻️ Refreshing...")
        try:
            data = stats.calculate_statistics()
            
            # Update cards
            self.stats_vars['events_var'].set(str(data['total_events']))
            self.stats_vars['commands_var'].set(str(data['total_commands']))
            self.stats_vars['processes_var'].set(str(data['total_processes']))
            self.stats_vars['files_var'].set(str(data['total_files']))  # ← جديد
            
            # Clear commands table
            for item in self.commands_table.get_children():
                self.commands_table.delete(item)
            
            # Add commands
            for cmd, count in data['top_commands']:
                display = cmd[:70] + "..." if len(cmd) > 70 else cmd
                self.commands_table.insert('', 'end', values=(display, count))
            
            # Clear files table 
            for item in self.files_table.get_children():
                self.files_table.delete(item)
            
            # Add files
            for filepath, count in data['top_files']:
                # Show only filename, not full path for cleaner display
                filename = filepath.split('/')[-1] if '/' in filepath else filepath
                # But show full path in tooltip (you can enhance this)
                display = filepath[:70] + "..." if len(filepath) > 70 else filepath
                self.files_table.insert('', 'end', values=(display, count))
            
            self.log_msg("✅ Refreshed")
            # update last update label
            try:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.header_labels['last_update'].config(text=f"Last Update: {now}")
            except Exception:
                pass

            # update new items list (files/folders created since last scan)
            try:
                from new_items_detector import find_new_items
                new = find_new_items(self.last_scan_time, max_items=50)
                self.new_items_list.delete(0, 'end')
                for it in new:
                    ts = it['ctime'].strftime('%H:%M') if it.get('ctime') else '--'
                    name = it['path'].split('/')[-1]
                    self.new_items_list.insert('end', f"{name} ({ts})")
                self.last_scan_time = datetime.now()
            except Exception:
                pass
        except Exception as e:
            self.log_msg(f"❌ Error: {e}")
    
    def toggle_auto(self):
        """Toggle auto update"""
        if not self.auto_running:
            self.auto_running = True
            self.auto_btn.config(text="⏸️ Stop Auto", bg=RED)
            threading.Thread(target=self._auto_loop, daemon=True).start()
            # Disable manual refresh while auto updates are running
            try:
                self.refresh_btn.config(state='disabled')
            except Exception:
                pass
            self.log_msg(f"▶️ Auto started ({AUTO_UPDATE_SECONDS}s)")
        else:
            self.auto_running = False
            self.auto_btn.config(text="▶️ Start Auto", bg=ORANGE)
            # Re-enable manual refresh
            try:
                self.refresh_btn.config(state='normal')
            except Exception:
                pass
            # analytics button should remain enabled
            self.log_msg("⏸️ Auto stopped")

    def _update_active_time_ui(self):
        try:
            active = self.usage_tracker.get_active_time()
            mins = int(active.total_seconds() // 60)
            hrs = mins // 60
            rem_m = mins % 60
            self.header_labels['active_time'].config(text=f"⏱️ Active Time: {hrs}h {rem_m}m")
        except Exception:
            pass
        # schedule again in 30 seconds
        try:
            self.root.after(30000, self._update_active_time_ui)
        except Exception:
            pass

    def open_analytics(self):
        """Open the analytics window using the analyzer."""
        try:
            gui_analytics_panel.create_analytics_window(self.root, self.analyzer)
        except Exception as e:
            self.log_msg(f"❌ Analytics error: {e}")
    
    def _auto_loop(self):
        """Auto update loop"""
        while self.auto_running:
            try:
                bash_collector.collect_and_save(db.save_event, MAX_BASH_COMMANDS)
                proc_collector.collect_and_save(db.save_event, MAX_PROCESSES)
                file_collector.collect_and_save(db.save_event, MAX_FILES)  # ← جديد
                self.root.after(0, self.refresh_view)
                time.sleep(AUTO_UPDATE_SECONDS)
            except:
                pass
    
    def export_csv(self):
        """Export to CSV"""
        try:
            filename = exporter.export_to_csv()
            if filename:
                self.log_msg(f"📤 Exported: {filename}")
                messagebox.showinfo("Success", f"Exported to:\n{filename}")
            else:
                raise Exception("Export failed")
        except Exception as e:
            self.log_msg(f"❌ Error: {e}")
            messagebox.showerror("Error", str(e))