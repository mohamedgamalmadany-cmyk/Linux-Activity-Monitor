#!/usr/bin/env python3
"""
Process Collector
Collects running processes only
"""

import subprocess
import json


def get_running_processes(max_processes=20):
    """Get list of running processes"""
    try:
        output = subprocess.check_output(['ps', 'aux'], text=True)
        lines = output.strip().split('\n')[1:]  # Skip header
        
        processes = []
        for line in lines[:max_processes]:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                processes.append({
                    'user': parts[0],
                    'cpu': parts[2],
                    'mem': parts[3],
                    'command': parts[10]
                })
        
        return processes
    except:
        return []


def collect_and_save(db_save_function, limit=5):
    """Collect processes and save to database"""
    processes = get_running_processes()
    
    for proc in processes[:limit]:
        db_save_function('running_process', json.dumps(proc))
    
    return len(processes[:limit])
