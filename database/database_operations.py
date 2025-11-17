#!/usr/bin/env python3
"""
Database Operations Only
Everything related to database is here
"""

import sqlite3
from datetime import datetime
from config import DB_FILE


def create_database():
    """Create database and tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            details TEXT NOT NULL
        )
    ''')
    
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON activity_log(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_event_type ON activity_log(event_type)')
    
    conn.commit()
    conn.close()


def save_event(event_type, details):
    """Save one event to database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            'INSERT INTO activity_log (timestamp, event_type, details) VALUES (?, ?, ?)',
            (timestamp, event_type, details)
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False


def get_all_events():
    """Get all events from database"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM activity_log ORDER BY timestamp DESC')
        events = cursor.fetchall()
        conn.close()
        return events
    except:
        return []


def delete_all_events():
    """Clear all data"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM activity_log')
        conn.commit()
        conn.close()
        return True
    except:
        return False
