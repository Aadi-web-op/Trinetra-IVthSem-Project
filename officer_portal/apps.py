from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class OfficerPortalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'officer_portal'

    def ready(self):
        # AI Keep-Alive daemon has been removed since Gemini is serverless.
        pass
