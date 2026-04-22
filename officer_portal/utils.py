from audit_logs.models import ImmutableLog
import logging

logger = logging.getLogger(__name__)

def verify_client_certificate(request):
    """
    Verifies the presence and validity of a client certificate.
    
    PHASE 4.5 UPDATE: CHECK DISABLED FOR DEPLOYMENT TESTING.
    Returns True to facilitate Azure load balancer testing.
    """
    return True, "Dev Bypass"

def log_officer_action(user, action, ip, metadata=None):
    """
    Centralized logger for officer actions to ImmutableLog.
    """
    if metadata is None:
        metadata = {}
        
    ImmutableLog.objects.create(
        actor=user if (user and user.is_authenticated) else None,
        action=action,
        ip=ip,
        metadata=metadata
    )
