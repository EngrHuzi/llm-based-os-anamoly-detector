from datetime import datetime
from config import REPORT_FILE


def save_report(analysis_text: str, df_summary: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(REPORT_FILE, 'a', encoding='utf-8') as f:
        f.write(f"\n{'=' * 70}\n")
        f.write(f"ANALYSIS CYCLE: {timestamp}\n")
        f.write(f"{'=' * 70}\n")
        f.write("PROCESS SNAPSHOT:\n")
        f.write(df_summary + "\n\n")
        f.write("GEMINI AI ANALYSIS:\n")
        f.write(analysis_text + "\n")
    print(f"  [*]  Report saved -> {REPORT_FILE}")
