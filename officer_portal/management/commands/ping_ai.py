from django.core.management.base import BaseCommand
from officer_portal.ai_service import analyze_logs
import time

class Command(BaseCommand):
    help = 'Pings the AI Node to keep it awake using the robust Service Layer'

    def handle(self, *args, **kwargs):
        self.stdout.write("🚀 Initiating AI Keep-Alive Ping...")
        
        try:
            # We use the service function because it already handles:
            # 1. Old gradio_client versions (The error you just saw)
            # 2. Retries (If AI is sleeping)
            # 3. Authentication Headers
            response = analyze_logs("PING-123", "Keep-Alive Ping")
            
            self.stdout.write(self.style.SUCCESS(f'✅ Ping Successful. Response: {str(response)[:100]}...'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Failed to ping AI Node: {e}'))
