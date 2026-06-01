from google import genai
from config import GEMINI_API_KEY
import pandas as pd

client = genai.Client(api_key=GEMINI_API_KEY)


def build_prompt(df: pd.DataFrame) -> str:
    log_text = df[['timestamp', 'pid', 'name', 'cpu_pct', 'memory_mb', 'delta_mb']].to_string(index=False)

    prompt = f"""
You are an expert operating system analyst specializing in memory leak detection.

Analyze the following process monitoring log captured from a live OS over multiple intervals:

{log_text}

Your task:
1. Identify any processes showing CONTINUOUS memory growth across multiple samples (classic memory leak signature).
2. Identify processes with UNUSUALLY HIGH memory usage for their process type.
3. Flag processes with LARGE positive delta_mb values (rapid memory spikes).
4. Ignore short-lived or stable processes (delta_mb near 0 consistently).

For EACH suspicious process, respond in this exact format:

ANOMALY DETECTED
PID: <pid>
Process: <name>
Memory Trend: <starting_mb>MB -> <current_mb>MB
Delta Pattern: <description of growth>
Suspected Issue: <memory leak / spike / abnormal usage>
Confidence: <LOW / MEDIUM / HIGH>
Recommended Action: <specific action to take>

If no anomalies are found, respond with: NO ANOMALIES DETECTED

Be specific, technical, and concise.
"""
    return prompt


def analyze_logs(df: pd.DataFrame) -> str:
    prompt = build_prompt(df)
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return f"[ERROR] Gemini API call failed: {str(e)}"
