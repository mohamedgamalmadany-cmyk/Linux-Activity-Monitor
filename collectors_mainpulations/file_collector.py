#!/usr/bin/env python3
"""
File Collector
Collects opened/accessed files only
"""

import subprocess
import os
import duplicate_checker


def get_open_files(max_files=50):
    """Get list of currently open files"""
    try:
        # Using lsof to get open files for current user
        username = os.getenv('USER')
        output = subprocess.check_output(
            ['lsof', '-u', username, '-F', 'n'],
            text=True,
            stderr=subprocess.DEVNULL
        )
        
        files = []
        for line in output.split('\n'):
            if line.startswith('n/'):  # File path starts with n/
                filepath = line[1:]  # Remove 'n' prefix
                
                # Filter only regular files (not sockets, pipes, etc.)
                if os.path.exists(filepath) and os.path.isfile(filepath):
                    # Skip system/temp files
                    if not any(x in filepath for x in ['/proc/', '/sys/', '/tmp/', '.sock']):
                        files.append(filepath)
        
        # Remove duplicates and limit
        files = list(set(files))[:max_files]
        return files
    except:
        return []


def get_recently_modified_files(directory="~", max_files=20):
    """Get recently modified files in home directory"""
    try:
        home = os.path.expanduser(directory)
        
        # Find files modified in last 24 hours
        output = subprocess.check_output(
            ['find', home, '-type', 'f', '-mtime', '-1', '-not', '-path', '*/.*'],
            text=True,
            stderr=subprocess.DEVNULL
        )
        
        files = [line.strip() for line in output.split('\n') if line.strip()]
        return files[:max_files]
    except:
        return []


def collect_and_save(db_save_function, limit=10):
    """Collect files and save to database"""
    files = get_open_files()
    
    for filepath in files[:limit]:
        try:
            h = duplicate_checker.make_hash('file_access', filepath)
            db_save_function('file_access', filepath, hash_value=h)
        except Exception:
            db_save_function('file_access', filepath)
    
    return len(files[:limit])
