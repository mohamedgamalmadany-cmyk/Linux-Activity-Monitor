#!/usr/bin/env python3
"""
System Resources Monitor
Provides simple psutil-based getters for CPU, memory, disk and network stats.
"""

import psutil


def get_cpu():
    """Return CPU percent (float)."""
    try:
        # short interval to get a near-instant value
        pct = psutil.cpu_percent(interval=0.3)
        return {'percent': round(pct, 1)}
    except Exception as e:
        return {'percent': 0.0, 'error': str(e)}


def get_memory():
    """Return memory usage info: percent, used, total (bytes)."""
    try:
        vm = psutil.virtual_memory()
        return {
            'percent': round(vm.percent, 1),
            'used': vm.used,
            'total': vm.total,
        }
    except Exception as e:
        return {'percent': 0.0, 'used': 0, 'total': 0, 'error': str(e)}


def get_disk(path='/'):
    """Return disk usage for given path: percent, used, total (bytes)."""
    try:
        du = psutil.disk_usage(path)
        return {
            'percent': round(du.percent, 1),
            'used': du.used,
            'total': du.total,
        }
    except Exception as e:
        return {'percent': 0.0, 'used': 0, 'total': 0, 'error': str(e)}


def get_network():
    """Return cumulative network I/O: bytes sent and received since boot."""
    try:
        net = psutil.net_io_counters()
        return {'sent': net.bytes_sent, 'recv': net.bytes_recv}
    except Exception as e:
        return {'sent': 0, 'recv': 0, 'error': str(e)}


def get_all(disk_path='/'):
    """Return all metrics in a single dict with convenient units.

    Memory and disk are annotated with _mb/_gb for display convenience.
    Network is returned with MB converted values as well.
    """
    try:
        cpu = get_cpu()
        mem = get_memory()
        disk = get_disk(disk_path)
        net = get_network()

        # convert bytes to MB/GB
        def to_mb(b):
            return round(b / (1024.0 ** 2), 2)

        def to_gb(b):
            return round(b / (1024.0 ** 3), 2)

        mem['used_mb'] = to_mb(mem.get('used', 0))
        mem['total_mb'] = to_mb(mem.get('total', 0))
        mem['used_gb'] = to_gb(mem.get('used', 0))
        mem['total_gb'] = to_gb(mem.get('total', 0))

        disk['used_mb'] = to_mb(disk.get('used', 0))
        disk['total_mb'] = to_mb(disk.get('total', 0))
        disk['used_gb'] = to_gb(disk.get('used', 0))
        disk['total_gb'] = to_gb(disk.get('total', 0))

        net_mb = {'sent_mb': to_mb(net.get('sent', 0)), 'recv_mb': to_mb(net.get('recv', 0))}

        return {'cpu': cpu, 'memory': mem, 'disk': disk, 'network': {**net, **net_mb}}
    except Exception as e:
        return {'error': str(e)}
