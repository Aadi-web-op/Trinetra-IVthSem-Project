from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from access_control.models import AllowedStation, TrapLog, BannedIP
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
        if request.path in ['/', '/health/']:
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

            # 1. Check if IP is permanently banned (Honeypot hit)
            if BannedIP.objects.filter(ip_address=client_ip).exists():
                return HttpResponseForbidden("INTRUSION DETECTED. IP IS BANNED.")
            
            # 2. Check Allowed Stations
            if AllowedStation.objects.filter(static_ip=client_ip, is_active=True).exists():
                 return self.get_response(request)

            # Not allowed: Log trap
            TrapLog.objects.create(
                ip_address=client_ip,
                attempted_username=request.user.username if request.user.is_authenticated else 'Anonymous',
                user_agent=request.META.get('HTTP_USER_AGENT', 'Unknown'),
                timestamp=timezone.now()
            )

            # For unauthenticated or unauthorized IPs, render the appropriate login page with IP_BLOCKED=True
            if request.path.startswith('/admin/'):
                return render(request, 'admin/login.html', {
                    'IP_BLOCKED': True,
                    'client_ip': client_ip
                }, status=403)
            else:
                return render(request, 'officer_portal/login.html', {
                    'IP_BLOCKED': True,
                    'client_ip': client_ip
                }, status=403)
            
        except Exception as e:
            logger.error(f"IPFortressMiddleware DB error: {e}")
            return self.get_response(request)

class ZeroTrustSessionMiddleware:
    """
    Prevents session hijacking by binding the session to IP and User-Agent.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            session_ip = request.session.get('zt_ip')
            session_ua = request.session.get('zt_ua')
            
            # If these don't exist, we might be from an old session, let's set them.
            if not session_ip or not session_ua:
                request.session['zt_ip'] = get_client_ip(request)
                request.session['zt_ua'] = request.META.get('HTTP_USER_AGENT', 'Unknown')
            else:
                current_ip = get_client_ip(request)
                current_ua = request.META.get('HTTP_USER_AGENT', 'Unknown')
                
                if current_ip != session_ip or current_ua != session_ua:
                    from django.contrib.auth import logout
                    logger.warning(f"Session Hijack Attempt Detected. Expected: {session_ip}/{session_ua}, Got: {current_ip}/{current_ua}")
                    logout(request)
                    return HttpResponseForbidden("SECURITY BREACH DETECTED: SESSION INVALIDATED.")
                    
        return self.get_response(request)
