"""
TRINETRA Health Check Endpoint
-------------------------------
Lightweight endpoint for Azure App Service health probes and monitoring.
Checks DB connectivity and returns system status.
"""
import time
import logging
from django.http import JsonResponse
from django.db import connection

logger = logging.getLogger('trinetra.health')


def health_check(request):
    """
    GET /health — Returns system health status.

    Used by:
    - Azure App Service health probes (keeps instance alive)
    - External monitoring (uptime checks)
    - Manual debugging (quick way to verify DB is reachable)
    """
    status = {
        'status': 'ok',
        'timestamp': time.time(),
        'checks': {}
    }
    http_status = 200

    # --- Check 1: Database Connectivity ---
    try:
        start = time.monotonic()
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        db_latency_ms = round((time.monotonic() - start) * 1000, 2)
        status['checks']['database'] = {
            'status': 'ok',
            'latency_ms': db_latency_ms
        }
        if db_latency_ms > 2000:
            status['checks']['database']['status'] = 'slow'
            logger.warning(f"Health check: DB latency is high ({db_latency_ms}ms)")
    except Exception as e:
        status['checks']['database'] = {
            'status': 'error',
            'error': str(e)
        }
        status['status'] = 'degraded'
        http_status = 503
        logger.error(f"Health check: DB connection failed — {e}")

    # --- Check 2: AI Service Config ---
    import os
    hf_token = os.getenv('HF_API_TOKEN')
    ai_node = os.getenv('TRINETRA_AI_NODE', '')
    status['checks']['ai_service'] = {
        'status': 'ok' if hf_token else 'misconfigured',
        'node_configured': bool(ai_node),
        'token_present': bool(hf_token),
    }
    if not hf_token:
        status['status'] = 'degraded'

    return JsonResponse(status, status=http_status)
