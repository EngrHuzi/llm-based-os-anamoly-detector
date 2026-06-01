import time
from monitor import get_process_snapshot, build_timeseries
from analyzer import analyze_logs
from alert import print_alert, get_severity
from report import save_report
from config import POLL_INTERVAL, SAMPLE_COUNT


def main():
    print("\n" + "=" * 70)
    print("  LLM-Based OS Log Anomaly Detector")
    print("  AI-Powered Memory Leak Detection using Google Gemini")
    print("=" * 70 + "\n")
    print(f"  [*]  Poll interval : {POLL_INTERVAL}s")
    print(f"  [*]  Samples/cycle : {SAMPLE_COUNT}")
    print(f"  [*]  Starting monitoring loop... (Ctrl+C to stop)\n")

    log_store = []
    cycle = 0

    while True:
        cycle += 1
        print(f"  [~]  Collecting snapshot {len(log_store) + 1}/{SAMPLE_COUNT} (Cycle {cycle})...")

        snapshot = get_process_snapshot()
        log_store.append(snapshot)

        if len(log_store) >= SAMPLE_COUNT:
            print(f"\n  [>]  Sending {SAMPLE_COUNT} snapshots to Gemini API for analysis...")

            df = build_timeseries(log_store)
            analysis = analyze_logs(df)

            print_alert(analysis)
            save_report(analysis, df.to_string())

            severity = get_severity(analysis)
            if severity in ["HIGH", "CRITICAL"]:
                print(f"  [!!] SEVERITY: {severity} — Immediate attention recommended!\n")

            log_store = log_store[-(SAMPLE_COUNT - 1):]

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  [X]  Monitoring stopped by user. Final report saved.")
