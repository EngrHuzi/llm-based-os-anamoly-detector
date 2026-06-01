# LLM-Based OS Log Anomaly Detector

AI-powered memory leak detector that monitors running OS processes in real-time and uses **Google Gemini** to analyze memory patterns and generate plain-English anomaly alerts.

## How It Works

1. **Collect** — `psutil` snapshots the top 20 processes every 5 seconds (Round Robin)
2. **Accumulate** — after 6 snapshots, builds a time-series DataFrame with `pandas` (including `delta_mb` per PID)
3. **Analyze** — sends the formatted log to Gemini API for AI-powered anomaly detection
4. **Alert** — prints structured alerts to the console and appends them to `anomaly_report.txt`

## Project Structure

```
llm-based-anamoly-detector/
├── main.py        # Entry point — starts the monitoring loop
├── monitor.py     # Process sampling via psutil, builds time-series DataFrame
├── analyzer.py    # Builds prompt and calls Gemini API
├── alert.py       # Formats and prints terminal alerts
├── report.py      # Appends analysis to anomaly_report.txt
├── config.py      # All configurable settings
├── pyproject.toml # uv project manifest
└── uv.lock
```

## Setup

```bash
# 1. Clone / enter the project
cd llm-based-anamoly-detector

# 2. Install dependencies (uv manages everything)
uv sync

# 3. Add your Gemini API key in config.py
#    Get a free key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "your-key-here"

# 4. Run
uv run python main.py
```

## Configuration (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `GEMINI_API_KEY` | `""` | Your Google Gemini API key |
| `POLL_INTERVAL` | `5` | Seconds between each process snapshot |
| `SAMPLE_COUNT` | `6` | Snapshots per analysis cycle |
| `TOP_PROCESSES` | `20` | Processes tracked per snapshot (sorted by RAM) |
| `REPORT_FILE` | `anomaly_report.txt` | Output file for saved reports |

## Anomaly Patterns Detected

| Pattern | Description |
|---|---|
| Monotonic Growth | RAM increases every sample — classic leak signature |
| Spike Detection | Large `delta_mb` vs historical baseline |
| Sustained High Usage | Process holds high RAM with no release |
| Contextual Reasoning | AI judges by process type (e.g. `chrome.exe` vs `sqlserver.exe`) |

## Sample Output

```
======================================================================
  AI ANOMALY ANALYSIS  |  2024-11-15 09:10:34
======================================================================

  [!!]  ANOMALY DETECTED
  --------------------------------------------------
  PID: 2456
  Process: chrome.exe
  Memory Trend: 312MB -> 2147MB
  Delta Pattern: Consistent +200-500MB growth per interval
  Suspected Issue: Memory leak — unreleased heap allocations
  Confidence: HIGH
  Recommended Action: Restart browser or audit installed extensions

======================================================================

  [*]  Report saved -> anomaly_report.txt
  [!!] SEVERITY: HIGH — Immediate attention recommended!
```

## Tech Stack

- **Python 3.13+**
- [`psutil`](https://pypi.org/project/psutil/) — process monitoring
- [`pandas`](https://pypi.org/project/pandas/) — time-series structuring
- [`google-generativeai`](https://pypi.org/project/google-generativeai/) — Gemini API (gemini-3.1-flash-lite)
- **uv** — dependency management

## OS Concept: Round Robin Scheduling

The monitoring loop mirrors Round Robin CPU scheduling — every process gets exactly one memory snapshot per cycle with `POLL_INTERVAL` acting as the time quantum. No process is starved, and slow background leaks (e.g. `svchost.exe`) are never skipped.
