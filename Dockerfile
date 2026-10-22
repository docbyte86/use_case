# TODO für Bewerber:
# 1. Passendes Base-Image wählen
# 2. Arbeitsverzeichnis & Dependencies einrichten
# 3. Quellcode kopieren
# 4. Security: Non-Root User setzen
# 5. CMD definieren

FROM python:3.11-slim

WORKDIR /app

# --- DEIN DOCKERFILE HIER ---

# Non-Root-User anlegen und nutzen (Sicherheit)
RUN useradd --create-home appuser

# Erst nur requirements kopieren und installieren (Layer-Caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dann den Code
COPY main.py .

# Auf den Non-Root-User wechseln
USER appuser

CMD ["python", "main.py"]