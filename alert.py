from datetime import datetime


def print_alert(analysis_text: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print("\n" + "=" * 70)
    print(f"  AI ANOMALY ANALYSIS  |  {timestamp}")
    print("=" * 70)

    if "NO ANOMALIES DETECTED" in analysis_text:
        print("  [OK]  No memory anomalies detected in this cycle.")
    else:
        blocks = analysis_text.strip().split("ANOMALY DETECTED")
        for block in blocks:
            if block.strip():
                print("\n  [!!]  ANOMALY DETECTED")
                print("-" * 50)
                for line in block.strip().splitlines():
                    if line.strip():
                        print(f"  {line.strip()}")

    print("=" * 70 + "\n")


def get_severity(analysis_text: str) -> str:
    for level in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if level in analysis_text.upper():
            return level
    return "NONE"
