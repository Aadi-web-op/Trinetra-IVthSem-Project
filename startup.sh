#!/bin/bash

# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Collect Static Files (CSS/JS)
python manage.py collectstatic --noinput

# 3. Apply Database Migrations (CRITICAL: Creates/Updates tables)
python manage.py migrate

# 4. Start the Server (Gunicorn)
# CRITICAL: --workers 1 is required because _ai_task_store is an in-memory dict.
# Multiple worker *processes* have separate memory; only threads within one process share it.
# --threads 8 lets us handle 8 concurrent requests without blocking.
# --timeout 600 allows AI requests to take up to 10 minutes.
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 1 --threads 8 config.wsgi:application
