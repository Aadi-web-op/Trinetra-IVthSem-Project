from django.apps import AppConfig
import threading
import time
import os
import logging

logger = logging.getLogger(__name__)


def keep_ai_awake():
    """
    Periodically pings the HF Space to prevent it from going to sleep.
    Runs as a daemon thread — automatically dies when the server shuts down.
    
    [PRODUCTION FIX] Added:
    - Initial 60s delay (let the server fully start before pinging)
    - Error resilience (single failure doesn't kill the loop)
    - Logging instead of print()
    """
    # Wait for server to fully start before first ping
    time.sleep(60)
    
    PING_INTERVAL = 43200  # 12 hours

    while True:
        try:
            from django.core.management import call_command
            call_command('ping_ai')
            logger.info("AI keep-alive ping succeeded.")
        except Exception as e:
            logger.warning(f"AI keep-alive ping failed (will retry in {PING_INTERVAL}s): {e}")
        
        try:
            time.sleep(PING_INTERVAL)
        except Exception:
            break  # Thread should die if sleep is interrupted


class OfficerPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'officer_portal'

    def ready(self):
        # [PRODUCTION FIX] Only start the keep-alive thread in the actual web server
        # process, NOT during migrations, collectstatic, or management commands.
        # RUN_MAIN is set by Django's autoreloader; in production (gunicorn),
        # we check that we're not running a management command by looking at argv.
        import sys

        is_management_command = any(
            cmd in sys.argv for cmd in ['migrate', 'collectstatic', 'createsuperuser', 'shell', 'test']
        )
        is_runserver_reload = os.environ.get('RUN_MAIN') == 'true'
        is_gunicorn = 'gunicorn' in sys.modules

        if (is_runserver_reload or is_gunicorn) and not is_management_command:
            daemon_thread = threading.Thread(target=keep_ai_awake, daemon=True, name='ai-keepalive')
            daemon_thread.start()
            logger.info("AI keep-alive daemon thread started.")
