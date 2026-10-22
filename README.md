haha
# Automated Health-Check & Service-Monitoring Pipeline

Dieses Repository dient als Grundlage und Vorlage für die 60-minütige Fallstudie im Rahmen des Auswahlverfahrens für die Position **Automation Engineer (m/w/d)**.

---

## 📋 Szenario & Aufgabenstellung

Ein interner Service (z. B. eine API für Infrastruktur-Status) soll automatisiert überwacht, die Daten verarbeitet und der Deployment-Prozess abgesichert werden.

### Deine Aufgaben (60 Minuten):

### 1. Automation & Data Fetching (Skript / Service)

* **Skripterstellung:** Erstelle eine kleine Automatisierung (z. B. in Python via `main.py`).
* **API-Abruf:** Rufe Daten von einer REST-API ab (z. B. `https://jsonplaceholder.typicode.com/todos` oder eine Mock-API) inkl. robustem Error Handling / Timeout-Management.
* **Transformation & Aggregation:** Filtere und transformiere die Daten (z. B. Identifikation von fehlerhaften/unerledigten States, Berechnung von Quoten) und ermittle einen Status (`HEALTHY` vs. `WARNING`).
* **Output:** Erstelle einen strukturierten JSON-Report oder Metrics-Payload über `stdout` / Datei.

### 2. Containerisierung & CI/CD-Workflow

* **Dockerfile:** Schreibe ein kompaktes und sicheres Dockerfile für deinen Service/Skript (schlankes Base-Image, Non-Root-User, Best Practices).
* **GitHub Actions Pipeline:** Erstelle/erweitere die Workflow-Datei (`.github/workflows/main.yml` bzw. `main.yaml`), die bei einem `push` auf den `main`-Branch automatisch:
  * Den Code prüft und testet (Syntax-Check / Unit Test / Linter).
  * Das Docker-Image baut.
  * Einen simulierten Deployment-Step oder eine Benachrichtigung (z. B. Webhook/Status-Echo) triggert.

### 3. Architektur-, Orchestrierungs- & Observability-Konzept (Stichpunkte/Skizze)

Beantworte kurz die folgenden konzeptionellen Fragen (in der README oder als separate Notiz/Whiteboard):

1. **Monitoring & Observability:** Wie würdest du diesen Service in eine moderne Monitoring-Landschaft (z. B. Grafana / Prometheus / OpenTelemetry / Loki) einbinden?
2. **Secret Management:** Wie gehst du mit Secrets (z. B. API-Tokens, Webhook-URLs, Credentials) im CI/CD-Prozess und zur Laufzeit sicher um?
3. **Orchestrierung:** Wie bettest du den Service auf einer Orchestrierungs-Plattform ein (z. B. Rundeck, n8n, Kubernetes CronJob, StackStorm)?

---

## 📂 Projektstruktur

```text
.
├── .github/
│   └── workflow/
│       └── main.yaml        # GitHub Actions CI/CD Pipeline
├── Dockerfile               # Container-Definition für den Health-Check Service
├── main.py                  # Python Automation- & Health-Check Skript
├── requirements.txt         # Python-Abhängigkeiten
└── README.md                # Dokumentation & Aufgabenstellung
```

---

## 🚀 Schnellstart (Lokal)

### Voraussetzungen

* Python 3.11+
* Docker (optional für Container-Test)

### Lokale Ausführung

```bash
# 1. Virtuelle Umgebung erstellen & Abhängigkeiten installieren
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Skript ausführen
python main.py
```

### Docker Ausführung

```bash
# Image bauen
docker build -t healthcheck-service:latest .

# Container starten
docker run --rm healthcheck-service:latest
```

---

## 📝 Konzept-Dokumentation (Notizen / Antworten)

### 1. Monitoring & Observability

* **Metriken & Tracing:** ...
* **Logging:** ...

### 2. Secret Management

* **CI/CD Pipeline:** ...
* **Runtime:** ...

### 3. Orchestrierung & Scheduling

* **Plattform-Integration:** ...
