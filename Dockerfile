# TODO für Bewerber:
# 1. Passendes Base-Image wählen
# 2. Arbeitsverzeichnis & Dependencies einrichten
# 3. Quellcode kopieren
# 4. Security: Non-Root User setzen
# 5. CMD definieren

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create a dedicated non-root group and user for security best practices
RUN groupadd --system appgroup && \
    useradd --system --gid appgroup --create-home appuser

# Install dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code and assign ownership to the non-root user
COPY --chown=appuser:appgroup main.py .

# Switch to the non-root user before runtime
USER appuser

CMD ["python", "main.py"]