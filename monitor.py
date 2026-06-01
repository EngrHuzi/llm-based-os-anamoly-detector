import psutil
import pandas as pd
from datetime import datetime
from config import TOP_PROCESSES


def get_process_snapshot():
    snapshot = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'status']):
        try:
            info = proc.info
            mem_mb = round(info['memory_info'].rss / (1024 * 1024), 2)
            snapshot.append({
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'pid':       info['pid'],
                'name':      info['name'],
                'cpu_pct':   info['cpu_percent'],
                'memory_mb': mem_mb,
                'status':    info['status']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    snapshot.sort(key=lambda x: x['memory_mb'], reverse=True)
    return snapshot[:TOP_PROCESSES]


def build_timeseries(log_store: list) -> pd.DataFrame:
    rows = []
    for snapshot in log_store:
        rows.extend(snapshot)

    df = pd.DataFrame(rows)
    df = df.sort_values(['pid', 'timestamp'])
    df['delta_mb'] = df.groupby('pid')['memory_mb'].diff().fillna(0).round(2)

    return df
