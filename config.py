import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

POLL_INTERVAL = 5
SAMPLE_COUNT = 6
TOP_PROCESSES = 20

MEMORY_UNIT = "MB"
REPORT_FILE = "anomaly_report.txt"

SEVERITY_LEVELS = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
