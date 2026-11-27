# Debian + Python 3.12, "slim" = ~150MB instead of ~1GB.
FROM python:3.12-slim

ENV PYTHONPATH=/app \
    # print() shows up in `docker compose logs` immediately
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# requirements.txt is copied ALONE first so Docker caches the pip install.
# Editing Python code then rebuilds in seconds instead of reinstalling everything.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Don't run as root inside the container.
RUN useradd --create-home --uid 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Exec (JSON) form so gunicorn is PID 1 and shuts down cleanly on `docker stop`.
# Workers: (2 x CPU cores) + 1.
CMD ["gunicorn", "main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "5", \
     "--timeout", "60", \
     "--keep-alive", "5", \
     "--bind", "0.0.0.0:8000"]
