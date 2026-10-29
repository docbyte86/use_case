import os
import sys
import logging
from typing import Any, Dict, List
import requests
import json
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# Logging-Setup (Standard-Out)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

API_URL = os.getenv("API_URL")
API_TIMEOUT = int(os.getenv("API_TIMEOUT"))
WARNING_THRESHOLD = float(os.getenv("WARNING_THRESHOLD"))

def fetch_todos(url: str, timeout: int = 5) -> List[Dict[str, Any]]:
    """Calls API and returns a list of todos."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Invalid API response format: expected a list of tasks.")

    return data

def evaluate_todos(
    todos: List[Dict[str, Any]], threshold: float = 0.60
) -> Dict[str, Any]:
    """Count open tasks, calculate ratios, and determine the service health status."""
    total_count = len(todos)

    if total_count == 0:
        return {
            "status": "HEALTHY",
            "metrics": {
                "total_tasks": 0,
                "open_tasks": 0,
                "completed_tasks": 0,
                "open_ratio": 0.0,
                "open_percentage": 0.0,
            },
        }

    # Count open tasks (completed == False)
    open_count = sum(1 for item in todos if not item.get("completed", False))
    completed_count = total_count - open_count
    open_ratio = open_count / total_count

    # Determine status (>= 60% open -> "WARNING", otherwise "HEALTHY")
    status = "WARNING" if open_ratio >= threshold else "HEALTHY"

    return {
        "status": status,
        "metrics": {
            "total_tasks": total_count,
            "open_tasks": open_count,
            "completed_tasks": completed_count,
            "open_ratio": round(open_ratio, 4),
            "open_percentage": round(open_ratio * 100, 2),
        },
    }

def run_healthcheck():
    """
    TODO für Bewerber:
    1. REST-API Daten abrufen (API_URL) & Fehler abfangen
    2. Offene Tasks (completed: false) zählen und Quote berechnen
    3. Status ermitteln (>= 60% offen -> "WARNING", sonst "HEALTHY")
    4. Ergebnis als strukturiertes JSON ausgeben
    """
    logging.info(f"Start health check for: {API_URL}")
    timestamp = datetime.now(timezone.utc).isoformat()

    try:
        todos = fetch_todos(API_URL, timeout=API_TIMEOUT)
        evaluation = evaluate_todos(todos, threshold=WARNING_THRESHOLD)

        report = {
            "timestamp": timestamp,
            "target_url": API_URL,
            "status": evaluation["status"],
            "threshold_open_ratio": WARNING_THRESHOLD,
            "metrics": evaluation["metrics"],
        }

        logging.info(
            f"Healthcheck completed: status={report['status']} "
            f"({report['metrics']['open_percentage']}% open)"
        )

        # Print structured JSON report to stdout
        print(json.dumps(report, indent=2))

    except requests.exceptions.Timeout:
        logging.error(f"Request timed out after {API_TIMEOUT}s while fetching {API_URL}")
        print(
            json.dumps(
                {
                    "timestamp": timestamp,
                    "target_url": API_URL,
                    "status": "ERROR",
                    "error": f"Request timed out after {API_TIMEOUT} seconds",
                },
                indent=2,
            )
        )
        sys.exit(1)

    except (requests.exceptions.RequestException, ValueError) as exc:
        logging.error(f"Healthcheck failed: {exc}")
        print(
            json.dumps(
                {
                    "timestamp": timestamp,
                    "target_url": API_URL,
                    "status": "ERROR",
                    "error": str(exc),
                },
                indent=2,
            )
        )
        sys.exit(1)

if __name__ == "__main__":
    run_healthcheck()