from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from access_control.models import AllowedStation, TrapLog
from access_control.utils import get_client_ip
from django.utils import timezone
from django.urls import resolve
import logging

logger = logging.getLogger(__name__)

class IPFortressMiddleware:
    """
    Blocks access from unauthorized IP addresses.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/health/':
            return self.get_response(request)

        # Allow static and media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # To test the IP Blocked UI locally, we can toggle this setting. 
        # If TRINETRA_STRICT_FIREWALL is False, bypass entirely.
        if not getattr(settings, 'TRINETRA_STRICT_FIREWALL', False):
            return self.get_response(request)

        try:
            client_ip = get_client_ip(request)
            
            if AllowedStation.objects.filter(static_ip=client_ip, is_active=True).exists():
                 return self.get_response(request)

            # Not allowed: Log trap
            TrapLog.objects.create(
                ip_address=client_ip,
                attempted_username=request.user.username if request.user.is_authenticated else 'Anonymous',
                user_agent=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                timestamp=timezone.now()
            )

            # For unauthenticated or unauthorized IPs, render the login page with IP_BLOCKED=True
            return render(request, 'officer_portal/login.html', {
                'IP_BLOCKED': True,
                'client_ip': client_ip
            }, status=403)
            
        except Exception as e:
            logger.error(f"IPFortressMiddleware DB error: {e}")
            return self.get_response(request)
