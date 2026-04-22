#!/bin/bash

# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Collect Static Files (CSS/JS)
python manage.py collectstatic --noinput

# 3. Apply Database Migrations (CRITICAL: Creates/Updates tables)
python manage.py migrate

# 4. Clean up stale AI tasks from previous crashes
python manage.py cleanup_tasks --max-age-minutes 60

# 5. Start the Server (Gunicorn)
# CRITICAL: --workers 1 is required because _ai_task_store is an in-memory dict.
# Multiple worker *processes* have separate memory; only threads within one process share it.
# --threads 8 lets us handle 8 concurrent requests without blocking.
# --timeout 600 allows AI requests to take up to 10 minutes.
# --keep-alive 65 matches Azure's 60s proxy keepalive (must be > proxy's value).
# --max-requests 1000 + --max-requests-jitter 50 prevents memory leaks by recycling workers.
# --graceful-timeout 30 gives in-flight requests time to finish on restart.
gunicorn \
    --bind=0.0.0.0:8000 \
    --timeout 600 \
    --workers 1 \
    --threads 8 \
    --keep-alive 65 \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --graceful-timeout 30 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    config.wsgi:application
