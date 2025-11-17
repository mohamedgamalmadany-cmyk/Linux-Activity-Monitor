#!/usr/bin/env python3
"""
Bash History Collector
Collects bash commands only
"""

import os


def get_bash_commands(max_commands=50):
    """Get bash command history"""
    try:
        home = os.path.expanduser("~")
        history_file = os.path.join(home, ".bash_history")
        
        if not os.path.exists(history_file):
            return []
        
        with open(history_file, 'r', encoding='utf-8', errors='ignore') as f:
            commands = [line.strip() for line in f if line.strip()]
        
        return commands[-max_commands:]
    except:
        return []


def collect_and_save(db_save_function, limit=10):
    """Collect bash commands and save to database"""
    commands = get_bash_commands()
    
    for cmd in commands[-limit:]:
        db_save_function('bash_command', cmd)
    
    return len(commands[-limit:])
