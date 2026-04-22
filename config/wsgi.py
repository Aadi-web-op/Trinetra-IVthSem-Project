import os

from django.core.wsgi import get_wsgi_application

import dotenv
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
app = application # Vercel looks for 'app'

# --- AUTO-SETUP FOR PRODUCTION (VERCEL/AZURE) ---
def run_setup():
    try:
        from django.core.management import call_command
        from django.contrib.auth import get_user_model
        
        # 1. Run Migrations
        print("Starting Auto-Migration...")
        call_command('migrate', interactive=False)
        
        # 2. Ensure Superuser Exists
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            print("Creating default admin user...")
            User.objects.create_superuser('admin', 'admin@trinetra.local', 'admin123')
            print("Admin user created successfully.")
            
    except Exception as e:
        print(f"Auto-Setup Error: {e}")

# Trigger setup
run_setup()
