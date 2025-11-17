#!/usr/bin/env python3
"""
Database Operations Only
Everything related to database is here
"""

import sqlite3
from datetime import datetime, timedelta
from config import DB_FILE


def create_database():
    """Create database and tables"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create table if missing
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            details TEXT NOT NULL
        )
    ''')

    # Ensure new columns exist (migrate if necessary)
    cursor.execute("PRAGMA table_info(activity_log)")
    cols = [r[1] for r in cursor.fetchall()]
    if 'hash' not in cols:
        try:
            cursor.execute('ALTER TABLE activity_log ADD COLUMN hash TEXT')
        except Exception:
            pass
    if 'session_id' not in cols:
        try:
            cursor.execute('ALTER TABLE activity_log ADD COLUMN session_id TEXT')
        except Exception:
            pass

    cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON activity_log(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_event_type ON activity_log(event_type)')
    # idx_hash may fail if column missing; wrap in try
    try:
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash ON activity_log(hash)')
    except Exception:
        pass
    
    conn.commit()
    conn.close()


def save_event(event_type, details, hash_value=None, session_id=None, skip_if_recent_minutes=5):
    """Save one event to database.

    If `hash_value` is provided, do a duplicate check and skip inserting
    if a record with the same hash exists within `skip_if_recent_minutes`.
    Backwards-compatible: callers may omit hash_value and session_id.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # duplicate check
        if hash_value:
            window_start = (datetime.now() - timedelta(minutes=skip_if_recent_minutes)).strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('SELECT id FROM activity_log WHERE hash = ? AND timestamp >= ?', (hash_value, window_start))
            if cursor.fetchone():
                conn.close()
                return False

        cursor.execute(
            'INSERT INTO activity_log (timestamp, event_type, details, hash, session_id) VALUES (?, ?, ?, ?, ?)',
            (timestamp, event_type, details, hash_value, session_id)
        )

        conn.commit()
        conn.close()

        # trim database size to limit
        try:
            trim_database_limit()
        except Exception:
            pass

        return True
    except Exception as e:
        print(f"Database error: {e}")
        return False


def trim_database_limit(max_records=1000):
    """Keep the activity_log table to at most `max_records` by deleting oldest entries."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM activity_log')
        total = cur.fetchone()[0]
        if total > max_records:
            # delete oldest rows
            to_delete = total - max_records
            cur.execute('DELETE FROM activity_log WHERE id IN (SELECT id FROM activity_log ORDER BY timestamp ASC LIMIT ?)', (to_delete,))
            conn.commit()
        conn.close()
    except Exception:
        pass


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
