# Automated Health-Check & Service-Monitoring Pipeline

Dieses Repository dient als Grundlage und Vorlage für die 60-minütige Fallstudie im Rahmen des Auswahlverfahrens für die Position **Automation Engineer (m/w/d)**.

---

## 📋 Szenario & Aufgabenstellung

Ein interner Service (z. B. eine API für Infrastruktur-Status) soll automatisiert überwacht, die Daten verarbeitet und der Deployment-Prozess abgesichert werden.

### Deine Aufgaben (60 Minuten):

### 1. Automation & Data Fetching (Skript / Service)

> 💡 **Freie Wahl der Skriptsprache:** Du kannst diese Aufgabe in der Programmier- bzw. Skriptsprache deiner Wahl lösen! Im Repository findest du Vorlagen für:
> * **Python:** `main.py`
> * **Bash / Shell:** `main.sh`
> * **PowerShell:** `main.ps1`
> 
> Nutze einfach die Vorlage/Sprache, mit der du am besten vertraut bist (oder erstelle eine eigene).

* **Skripterstellung:** Implementiere die Automatisierungslogik in deiner gewählten Sprache (z. B. `main.py`, `main.sh` oder `main.ps1`).
* **API-Abruf:** Rufe Daten von einer REST-API ab (z. B. `https://jsonplaceholder.typicode.com/todos` oder eine Mock-API) inkl. robustem Error Handling / Timeout-Management.
* **Transformation & Aggregation:** Filtere und transformiere die Daten (z. B. Identifikation von fehlerhaften/unerledigten States, Berechnung von Quoten) und ermittle einen Status (`HEALTHY` vs. `WARNING`).
* **Output:** Erstelle einen strukturierten JSON-Report oder Metrics-Payload über `stdout` / Datei.

### 2. Containerisierung & CI/CD-Workflow

* **Dockerfile:** Schreibe ein kompaktes und sicheres Dockerfile für deinen Service/Skript passend zu deiner gewählten Sprache/Runtime (schlankes Base-Image, Non-Root-User, Best Practices).
* **GitHub Actions Pipeline:** Erstelle/erweitere die Workflow-Datei (`.github/workflows/main.yml` bzw. `.github/workflow/main.yaml`), die bei einem `push` auf den `main`-Branch automatisch:
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
├── main.ps1                 # PowerShell Automation- & Health-Check Skript
├── main.py                  # Python Automation- & Health-Check Skript
├── main.sh                  # Bash/Shell Automation- & Health-Check Skript
├── requirements.txt         # Python-Abhängigkeiten (bei Python-Nutzung)
└── README.md                # Dokumentation & Aufgabenstellung
```

---

## 🚀 Schnellstart (Lokal)

### Voraussetzungen

Je nach gewählter Skriptsprache:
* **Python:** Python 3.11+
* **Bash:** Bash, `curl`, `jq`
* **PowerShell:** PowerShell (`pwsh`) 7+
* **Docker:** Optional für lokale Container-Tests

### Lokale Ausführung

Wähle die passende Ausführung für deine gewählte Skriptsprache:

#### Option A: Python (`main.py`)
```bash
# macOS / Linux: virtuelle Umgebung erstellen und aktivieren
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```powershell
# Windows PowerShell: virtuelle Umgebung erstellen und aktivieren
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

```bash
# macOS / Linux: Skript in der aktivierten virtuellen Umgebung ausführen
python main.py
```

Ohne weitere Konfiguration verwendet das Python-Skript die JSONPlaceholder-Todos-API,
ein Timeout von 5 Sekunden und einen Warnschwellwert von 60 %. Diese Werte lassen
sich über `API_URL`, `API_TIMEOUT` und `WARNING_THRESHOLD` als Umgebungsvariablen überschreiben.
Eine `.env`-Datei im Projektverzeichnis wird beim Start automatisch geladen; bereits
gesetzte Umgebungsvariablen haben Vorrang. Lege Geheimnisse wie API-Schlüssel nur lokal
in `.env` ab und committe die Datei nicht.

#### Option B: Bash (`main.sh`)
```bash
chmod +x main.sh
./main.sh
```

#### Option C: PowerShell (`main.ps1`)
```powershell
pwsh ./main.ps1
```

### Docker Ausführung

*(Passe das `Dockerfile` ggf. an deine gewählte Sprache / Runtime an)*

```bash
# Image bauen
docker build -t healthcheck-service:latest .

# Container starten
docker run --rm healthcheck-service:latest
```

---

## 📝 Konzept-Dokumentation (Notizen / Antworten)

### 1. Monitoring & Observability

- **Metriken & Tracing:**
  - **Metriken-Erfassung:** Da das Skript als kurzlebiger Batch-/Cron-Job läuft, werden die ermittelten Kennzahlen (`total_tasks`, `open_tasks`, `open_ratio`, HTTP-Latenz sowie der Status als Gauge `0=HEALTHY`, `1=WARNING`, `2=ERROR`) am Ende des Laufs an ein **Prometheus Pushgateway** oder via **OpenTelemetry SDK (OTLP)** an einen **OpenTelemetry Collector** gesendet. Alternativ kann das Skript als dauerhafter Microservice mit eigenem `/metrics`-Endpoint (`prometheus_client`) betrieben werden.
  - **Tracing:** Über OpenTelemetry (`opentelemetry-instrumentation-requests`) werden ausgehende API-Aufrufe mit einer `trace_id` versehen, um Latenzen und Timeouts Ende-zu-Ende (z. B. in **Grafana Tempo** oder **Jaeger**) nachvollziehen zu können.
  - **Visualisierung & Alerting:** In **Grafana** visualisiert ein Dashboard den zeitlichen Verlauf der `open_ratio`. Über den **Prometheus Alertmanager** (oder Grafana Alerting) werden Alarme ausgelöst, sobald der Status auf `WARNING`/`ERROR` wechselt oder der Job ausbleibt (*Dead Man's Switch* via `absent()`-Query).
- **Logging:**
  - **12-Factor-App Logging:** Der Container schreibt alle Laufzeit-Logs auf `stderr` und das strukturierte Ergebnis-JSON auf `stdout` (keine lokalen Log-Dateien im Container).
  - **Zentrale Aggregation:** Ein leichtgewichtiger Log-Agent (**Grafana Alloy**, **Promtail** oder **Fluent Bit**) greift die Container-Streams ab, reichert sie mit Metadaten (Container-Name, Commit-SHA, Environment) an und leitet sie an **Grafana Loki** weiter. Dort lassen sich per *LogQL* gezielt fehlerhafte Läufe (`status="ERROR"`) filtern und auswerten.

### 2. Secret Management

- **CI/CD Pipeline:**
  - **Vermeidung von Klartext-Secrets:** Keine Ablage von API-Keys, Passwörtern oder Webhook-URLs im Git-Repository (Absicherung durch *GitHub Secret Scanning* und `gitleaks` als Pre-Commit-Hook).
  - **Geschützte Speicherung & OIDC:** Sensible Variablen werden in **GitHub Actions Secrets** (gebunden an geschützte *GitHub Environments* wie `production`) hinterlegt. Für den Zugriff auf Cloud-Ressourcen, Container-Registries oder einen zentralen Vault wird **OIDC (OpenID Connect)** genutzt, um kurzlebige, dynamische Tokens statt statischer Langzeit-Credentials zu verwenden.
- **Runtime:**
  - **Image-Sicherheit:** Secrets werden niemals per `ENV` oder `ARG` in das `Dockerfile` eingebaut, da sie sonst in den Image-Layern (`docker history`) sichtbar wären.
  - **Dynamische Injektion:** Zur Laufzeit werden Secrets aus einem zentralen Secret Store (**HashiCorp Vault**, **AWS Secrets Manager**, **Azure Key Vault** oder **Kubernetes Secrets** via *External Secrets Operator*) abgerufen und dem Container ausschließlich im Arbeitsspeicher (`tmpfs`-Volume oder geschützte Environment-Variablen) nach dem *Least-Privilege-Prinzip* bereitgestellt.

### 3. Orchestrierung & Scheduling

- **Plattform-Integration:**
  - **Cloud-Native (Kubernetes CronJob):** Bereitstellung als `CronJob`-Ressource (z. B. `schedule: "*/5 * * * *"`). Wichtige Einstellungen für den Produktionsbetrieb:
    - `concurrencyPolicy: Forbid` (verhindert überlappende Läufe bei langsamer API).
    - `restartPolicy: OnFailure` mit definiertem `backoffLimit`.
    - Strikte `resources` (Requests/Limits für CPU & Memory) sowie `securityContext` (`runAsNonRoot: true`, `readOnlyRootFilesystem: true`).
  - **Workflow- & Event-Driven Automation (Rundeck / StackStorm / n8n):**
    - Ausführung des Containers als geplanter Job in **Rundeck**, **StackStorm** oder **n8n**.
    - **Auto-Remediation & Incident-Flow:** Die Plattform wertet den Exit-Code (`0` vs. `1`) sowie den JSON-Output auf `stdout` direkt aus. Bei `"status": "WARNING"` oder `"ERROR"` triggert der Workflow automatisch Folgeschritte – etwa ein Remediation-Playbook (z. B. Skalierung oder Neustart von Worker-Instanzen), eine Benachrichtigung in Slack/MS Teams oder die automatische Ticket-Erstellung in Jira/ServiceNow.


    ---English---
## 📝 Concept Documentation (Notes / Answers)

### 1. Monitoring & Observability

- **Metrics & Tracing:**
  - **Metrics Collection:** Because the script runs as a short-lived batch/scheduled job, calculated metrics (`total_tasks`, `open_tasks`, `open_ratio`, HTTP latency, and health status encoded as `0=HEALTHY`, `1=WARNING`, `2=ERROR`) are pushed upon completion to a **Prometheus Pushgateway** or via the **OpenTelemetry SDK (OTLP)** to an **OpenTelemetry Collector**. Alternatively, the script can be wrapped as a long-running service exposing a `/metrics` endpoint via `prometheus_client`.
  - **Tracing:** Outbound HTTP requests are instrumented using OpenTelemetry (`opentelemetry-instrumentation-requests`) to propagate a `trace_id`, enabling end-to-end latency and timeout analysis in **Grafana Tempo** or **Jaeger**.
  - **Visualization & Alerting:** **Grafana** dashboards track `open_ratio` trends over time. **Prometheus Alertmanager** triggers alerts whenever the status switches to `WARNING`/`ERROR` or if expected job executions are missing (*Dead Man's Switch* using Prometheus `absent()` queries).
- **Logging:**
  - **12-Factor App Logging:** The container writes execution logs to `stderr` and the structured JSON report to `stdout` without persisting local log files inside the container.
  - **Centralized Log Aggregation:** A log shipper (**Grafana Alloy**, **Promtail**, or **Fluent Bit**) scrapes the container streams, enriches them with metadata labels (`service`, `env`, `commit_sha`), and forwards them to **Grafana Loki** for *LogQL* querying and log-based alerting.

### 2. Secret Management

- **CI/CD Pipeline:**
  - **Zero Secrets in Git:** API tokens, credentials, and webhook URLs are strictly excluded from version control (enforced via *GitHub Secret Scanning* and `gitleaks` pre-commit checks).
  - **Encrypted Secrets & OIDC:** Sensitive pipeline variables are stored in **GitHub Actions Encrypted Secrets** scoped to protected **GitHub Environments**. Instead of static long-lived keys, the pipeline uses **OIDC (OpenID Connect)** to request short-lived, dynamic tokens from cloud providers, registries, or HashiCorp Vault.
- **Runtime:**
  - **Image Hygiene:** Secrets are never baked into the `Dockerfile` via `ENV` or `ARG` instructions to prevent leakage through image layers (`docker history`).
  - **Dynamic Runtime Injection:** At container startup, secrets are dynamically fetched from a dedicated secret manager (**HashiCorp Vault**, **AWS Secrets Manager**, **Azure Key Vault**, or **Kubernetes Secrets** synced via the *External Secrets Operator*) and injected as environment variables or in-memory `tmpfs` mounts following the **Principle of Least Privilege**.

### 3. Orchestration & Scheduling

- **Platform Integration:**
  - **Cloud-Native (Kubernetes CronJob):** Deployed as a Kubernetes `CronJob` (e.g., `schedule: "*/5 * * * *"`). Key production settings include:
    - `concurrencyPolicy: Forbid` to prevent overlapping runs if the upstream API responds slowly.
    - `restartPolicy: OnFailure` with a bounded `backoffLimit`.
    - Enforced `resources` (CPU/Memory requests and limits) and a hardened `securityContext` (`runAsNonRoot: true`, `readOnlyRootFilesystem: true`).
  - **Event-Driven Automation & Remediation (Rundeck / StackStorm / n8n):**
    - Integrated as a scheduled job step within **Rundeck**, **StackStorm**, or **n8n**.
    - **Automated Remediation:** The orchestration platform parses both the container exit code (`0` vs. `1`) and the structured JSON payload on `stdout`. If `"status": "WARNING"` or `"ERROR"` is detected, the workflow branches automatically to trigger self-healing playbooks (e.g., scaling worker nodes, restarting stuck queues), send Slack/Teams notifications, or create an incident ticket in Jira/ServiceNow.