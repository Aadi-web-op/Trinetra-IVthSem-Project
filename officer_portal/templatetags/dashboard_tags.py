from django import template
from django.conf import settings
from audit_logs.models import ImmutableLog

register = template.Library()

@register.simple_tag
def get_security_status():
    """
    Returns critical security indicators for the dashboard.
    """
    return {
        'debug_mode': getattr(settings, 'DEBUG', False),
        'firewall_active': getattr(settings, 'TRINETRA_STRICT_FIREWALL', False),
        'secure_cookies': getattr(settings, 'SESSION_COOKIE_SECURE', False),
        'allowed_hosts': getattr(settings, 'ALLOWED_HOSTS', []),
    }

@register.simple_tag
def get_audit_feed(limit=5):
    """
    Returns the latest immutable logs for the Intel Feed.
    """
    try:
        return ImmutableLog.objects.select_related('user').order_by('-timestamp')[:limit]
    except Exception:
        return []
