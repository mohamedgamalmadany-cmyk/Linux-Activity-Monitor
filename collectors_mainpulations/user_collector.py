#!/usr/bin/env python3
"""
User Collector
Collects logged in users only
"""

import subprocess


def get_logged_users():
    """Get currently logged in users"""
    try:
        output = subprocess.check_output(['w', '-h'], text=True)
        users = [line.strip() for line in output.strip().split('\n') if line.strip()]
        return users
    except:
        return []


def collect_and_save(db_save_function):
    """Collect users and save to database"""
    users = get_logged_users()
    
    for user in users:
        db_save_function('logged_user', user)
    
    return len(users)
