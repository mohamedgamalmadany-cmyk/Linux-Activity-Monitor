#!/usr/bin/env python3
"""
CSV Exporter
Exports data to CSV files only
"""

import csv
import sqlite3
from datetime import datetime
from config import DB_FILE


def export_to_csv(limit=1000):
    """Export data to CSV file"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT {limit}')
        rows = cursor.fetchall()
        
        filename = f'activity_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Timestamp', 'Event Type', 'Details'])
            writer.writerows(rows)
        
        conn.close()
        return filename
    except Exception as e:
        print(f"Export error: {e}")
        return None
