#!/usr/bin/env python3
"""
Detect newly created files and folders since a given timestamp.
Scans the user's home directory for items with creation time after `since`.
"""

import os
from datetime import datetime


def find_new_items(since_dt, max_items=50, search_dir=None):
    """Return list of new items (path, is_dir, ctime) since `since_dt`.

    `since_dt` should be a datetime.datetime object.
    """
    try:
        home = os.path.expanduser('~') if search_dir is None else os.path.expanduser(search_dir)
        results = []
        since_ts = since_dt.timestamp()
        for root, dirs, files in os.walk(home):
            # check dirs
            for d in dirs:
                path = os.path.join(root, d)
                try:
                    st = os.stat(path)
                    if st.st_ctime >= since_ts:
                        results.append({'path': path, 'is_dir': True, 'ctime': datetime.fromtimestamp(st.st_ctime)})
                        if len(results) >= max_items:
                            return results
                except Exception:
                    continue
            for f in files:
                path = os.path.join(root, f)
                try:
                    st = os.stat(path)
                    if st.st_ctime >= since_ts:
                        results.append({'path': path, 'is_dir': False, 'ctime': datetime.fromtimestamp(st.st_ctime)})
                        if len(results) >= max_items:
                            return results
                except Exception:
                    continue
        return results
    except Exception:
        return []
