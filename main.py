import os
import sys
import logging
import requests
import json

# Logging-Setup (Standard-Out)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

API_URL = os.getenv("API_URL", "https://jsonplaceholder.typicode.com/todos")

def fetch_data(url: str) -> list:
    """Holt die Daten von der API, mit Timeout und Fehlerbehandlung."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("Zeitüberschreitung beim API-Abruf.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logging.error(f"Fehler beim API-Abruf: {e}")
        sys.exit(1)


def analyze(todos: list) -> dict:
    """Transformiert die Daten und ermittelt den Health-Status."""
    total = len(todos)
    completed = sum(1 for t in todos if t.get("completed") is True)
    open_tasks = total - completed
    open_rate = round((open_tasks / total) * 100, 2) if total > 0 else 0

    # Schwellenwert laut Vorgabe: >= 60% offen -> WARNING
    status = "WARNING" if open_rate >= 60 else "HEALTHY"

    return {
        "status": status,
        "total_tasks": total,
        "completed_tasks": completed,
        "open_tasks": open_tasks,
        "open_rate_percent": open_rate,
    }

def run_healthcheck():
    """Führt den Healthcheck aus: Daten abrufen, analysieren und als JSON ausgeben."""

    logging.info(f"Starte Healthcheck für: {API_URL}")
    todos = fetch_data(API_URL)
    report = analyze(todos)
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    run_healthcheck()
