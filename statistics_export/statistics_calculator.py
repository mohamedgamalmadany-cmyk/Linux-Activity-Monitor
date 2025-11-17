#!/usr/bin/env python3
"""
Statistics Calculator
Calculates statistics from database only
"""

import sqlite3
from config import DB_FILE


def calculate_statistics():
    """Calculate all statistics"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Total events
        cursor.execute('SELECT COUNT(*) FROM activity_log')
        total_events = cursor.fetchone()[0]
        
        # Total commands
        cursor.execute("SELECT COUNT(*) FROM activity_log WHERE event_type='bash_command'")
        total_commands = cursor.fetchone()[0]
        
        # Total processes
        cursor.execute("SELECT COUNT(*) FROM activity_log WHERE event_type='running_process'")
        total_processes = cursor.fetchone()[0]
        
        # Total files ← جديد
        cursor.execute("SELECT COUNT(*) FROM activity_log WHERE event_type='file_access'")
        total_files = cursor.fetchone()[0]
        
        # Top 5 commands
        cursor.execute('''
            SELECT details, COUNT(*) as count
            FROM activity_log
            WHERE event_type = 'bash_command'
            GROUP BY details
            ORDER BY count DESC
            LIMIT 5
        ''')
        top_commands = cursor.fetchall()
        
        # Top 5 files 
        cursor.execute('''
            SELECT details, COUNT(*) as count
            FROM activity_log
            WHERE event_type = 'file_access'
            GROUP BY details
            ORDER BY count DESC
            LIMIT 5
        ''')
        top_files = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_events': total_events,
            'total_commands': total_commands,
            'total_processes': total_processes,
            'total_files': total_files,  
            'top_commands': top_commands,
            'top_files': top_files  
        }
    except:
        return {
            'total_events': 0,
            'total_commands': 0,
            'total_processes': 0,
            'total_files': 0,  
            'top_commands': [],
            'top_files': []  
        }
