# LLM-Based OS Anomaly Detector

> AI-powered memory leak detector that monitors live OS processes and uses **Google Gemini** to analyze memory trends and generate plain-English anomaly alerts.

![Python](https://img.shields.io/badge/Python-3.13%2B-blue)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## How It Works

```
OS Processes
    │
    ▼
psutil snapshot (every 5s)
    │
    ▼
Pandas timeseries (delta_mb per PID)
    │
    ▼
Gemini API — anomaly analysis prompt
    │
    ▼
Console alert + anomaly_report.txt
```

1. **Monitor** — Polls the top 20 memory-consuming processes every `POLL_INTERVAL` seconds using `psutil`.
2. **Accumulate** — After `SAMPLE_COUNT` snapshots, builds a Pandas DataFrame with a computed `delta_mb` column (per-PID memory change between intervals).
3. **Analyze** — Sends the formatted timeseries to Gemini with a structured expert prompt asking it to flag continuous growth, sudden spikes, and abnormally high usage.
4. **Alert** — Prints a formatted anomaly report to the console with severity classification (LOW / MEDIUM / HIGH / CRITICAL).
5. **Report** — Appends every analysis cycle to `anomaly_report.txt` for a persistent audit trail.

---

## Project Structure

```
llm-based-anamoly-detector/
├── main.py          # Entry point — main monitoring loop
├── monitor.py       # psutil snapshot collection & timeseries builder
├── analyzer.py      # Gemini prompt construction & API call
├── alert.py         # Console alert formatting & severity extraction
├── report.py        # Append-mode report file writer
├── config.py        # All settings (intervals, counts, API key)
├── pyproject.toml   # uv project manifest & dependencies
└── uv.lock          # Locked dependency tree
```

---

## Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) — fast Python package manager
- A [Google Gemini API key](https://aistudio.google.com/app/apikey) (free tier available)

### Install

```bash
git clone https://github.com/EngrHuzi/llm-based-os-anamoly-detector.git
cd llm-based-os-anamoly-detector
uv sync
```

### Configure

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> Get a free key at [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Run

```bash
uv run python main.py
```

Press `Ctrl+C` to stop. A final report is saved automatically.

---

## Configuration

All settings live in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `POLL_INTERVAL` | `5` | Seconds between each process snapshot |
| `SAMPLE_COUNT` | `6` | Snapshots per analysis cycle (~30s window) |
| `TOP_PROCESSES` | `20` | Top memory processes tracked per snapshot |
| `REPORT_FILE` | `anomaly_report.txt` | Output file for saved analysis history |

---

## Anomaly Patterns Detected

| Pattern | Description |
|---|---|
| **Monotonic Growth** | RAM increases every sample — classic memory leak signature |
| **Spike Detection** | Large `delta_mb` vs. baseline — sudden memory surge |
| **Sustained High Usage** | Process holds abnormally high RAM without releasing it |
| **Contextual Reasoning** | Gemini judges by process type (`chrome.exe` vs `svchost.exe` differ in expected baseline) |

---

## Sample Output

```
======================================================================
  LLM-Based OS Log Anomaly Detector
  AI-Powered Memory Leak Detection using Google Gemini
======================================================================

  [*]  Poll interval : 5s
  [*]  Samples/cycle : 6
  [*]  Starting monitoring loop... (Ctrl+C to stop)

  [~]  Collecting snapshot 6/6 (Cycle 1)...

  [>]  Sending 6 snapshots to Gemini API for analysis...

======================================================================
  AI ANOMALY ANALYSIS  |  2026-06-02 14:32:10
======================================================================

  [!!]  ANOMALY DETECTED
  --------------------------------------------------
  PID: 4821
  Process: chrome.exe
  Memory Trend: 312MB -> 2147MB
  Delta Pattern: Consistent +200–500MB growth per interval
  Suspected Issue: Memory leak — unreleased heap allocations
  Confidence: HIGH
  Recommended Action: Restart browser or audit installed extensions

======================================================================
  [*]  Report saved -> anomaly_report.txt
  [!!] SEVERITY: HIGH — Immediate attention recommended!
```

---

## Tech Stack

| Tool | Role |
|---|---|
| `psutil` | Cross-platform process & memory monitoring |
| `pandas` | Timeseries construction and `delta_mb` computation |
| `google-genai` | Gemini API client for AI analysis |
| `python-dotenv` | `.env` file loading for API key management |
| `uv` | Fast dependency management & virtual environments |

---

## OS Concept: Round Robin Scheduling

The monitoring loop mirrors **Round Robin CPU scheduling** — every process gets one memory snapshot per cycle, with `POLL_INTERVAL` acting as the time quantum. No process is ever skipped, ensuring that slow background leaks (e.g. `svchost.exe`) are always captured alongside high-activity processes.

---

## License

MIT — free to use, modify, and distribute.
