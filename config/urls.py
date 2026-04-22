from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from access_control.views import trap_login, root_routing_view
from officer_portal.views import AdminLoginOverrideView
from config.health import health_check

urlpatterns = [
    # Health Check (Azure probes + monitoring)
    path('health/', health_check, name='health_check'),

    # Root Routing: Smart Redirect based on Client IP
    path('', root_routing_view, name='root_redirect'),

    # HIJACK: Force Admin Login to use our clean custom view
    path('admin/login/', AdminLoginOverrideView.as_view(), name='admin_login'),

    path('admin/', admin.site.urls),
    path('portal/', include('officer_portal.urls')),
    path('auth/', include('authentication.urls')),
    path('accounts/login/', trap_login, name='trap_login'),
]
