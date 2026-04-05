from django.shortcuts import render, redirect
from django.conf import settings
from .utils import get_client_ip
from .models import AllowedStation

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
    
    if getattr(settings, 'DEBUG', False) or \
       not getattr(settings, 'TRINETRA_STRICT_FIREWALL', False) or \
       AllowedStation.objects.filter(static_ip=client_ip, is_active=True).exists():
        return redirect('portal_login') 
    else:
        return redirect('trap_login')
