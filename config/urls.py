from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from access_control.views import trap_login, root_routing_view, honeypot_tarpit
from officer_portal.views import AdminLoginOverrideView
from config.health import health_check
from config.admin_site import trinetra_admin

# Auto-discover admin registrations from all apps, register on our custom site
admin.site = trinetra_admin
admin.autodiscover()

urlpatterns = [
    # Health Check (Azure probes + monitoring)
    path('health/', health_check, name='health_check'),

    # Root Routing: Smart Redirect based on Client IP
    path('', root_routing_view, name='root_redirect'),

    # HIJACK: Force Admin Login to use our clean custom view
    path('admin/login/', AdminLoginOverrideView.as_view(), name='admin_login'),

    path('admin/', trinetra_admin.urls),
    path('portal/', include('officer_portal.urls')),
    path('auth/', include('authentication.urls')),
    path('accounts/login/', trap_login, name='trap_login'),

    # Honeypot Endpoints
    path('api/v1/export_all_cases/', honeypot_tarpit),
    path('admin/db_dump/', honeypot_tarpit),
    path('wp-admin/', honeypot_tarpit),
    path('.env', honeypot_tarpit),
]

