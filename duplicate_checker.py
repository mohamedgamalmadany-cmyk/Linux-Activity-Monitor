#!/usr/bin/env python3
"""
Duplicate checker utilities.
Generates a hash for an event and checks database for recent duplicates.
"""

import hashlib
from database import database_operations as db


def make_hash(event_type, details):
    h = hashlib.sha256()
    h.update((event_type + '||' + details).encode('utf-8'))
    return h.hexdigest()


def is_recent_duplicate(hash_value, minutes=5):
    """Return True if a record with `hash_value` exists within the last `minutes` minutes."""
    try:
        # reuse save_event duplicate logic indirectly by querying DB
        conn = __import__('sqlite3').connect(db.DB_FILE)
        cur = conn.cursor()
        from datetime import datetime, timedelta
        window_start = (datetime.now() - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')
        cur.execute('SELECT id FROM activity_log WHERE hash = ? AND timestamp >= ?', (hash_value, window_start))
        exists = cur.fetchone() is not None
        conn.close()
        return exists
    except Exception:
        return False
