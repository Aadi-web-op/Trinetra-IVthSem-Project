from django.shortcuts import render, redirect
from django.conf import settings
from .utils import get_client_ip
from .models import AllowedStation, BannedIP, TrapLog
from django.http import HttpResponseForbidden

def trap_login(request):
    """
    The view for the trap login page.
    """
    return render(request, 'trap_login.html')

def root_routing_view(request):
    """
    Smart Redirect based on IP Authorization.
    """
    client_ip = get_client_ip(request)
    
    # The middleware allows '/' through without checking IPs so the public can see the landing page.
    # The actual IP blocking happens when they try to access /admin/ or /portal/ endpoints.
    return render(request, 'landing.html')

def honeypot_tarpit(request):
    """
    Intrusion Tarpit: Any IP hitting this endpoint is instantly banned.
    """
    client_ip = get_client_ip(request)
    
    # Don't ban allowed stations even if they hit the honeypot by accident
    if not AllowedStation.objects.filter(static_ip=client_ip, is_active=True).exists():
        BannedIP.objects.get_or_create(
            ip_address=client_ip,
            defaults={'reason': f'Hit honeypot at {request.path}'}
        )
        TrapLog.objects.create(
            ip_address=client_ip,
            attempted_username='HONEYPOT_SCANNER',
            user_agent=request.META.get('HTTP_USER_AGENT', 'Unknown')
        )
        
    return HttpResponseForbidden("INTRUSION DETECTED. IP LOGGED AND BANNED.")
