import time
from django.utils import timezone
from datetime import timedelta

def trinetra_context(request):
    """
    Global context processor for Trinetra UI.
    Provides variables like clearance level, session expiry, etc.
    """
    context = {}
    
    if request.user.is_authenticated:
        # Determine clearance level based on user status
        # In a real app, this would be a field on the custom User model
        if request.user.is_superuser:
            context['clearance_level'] = 4
        elif request.user.is_staff:
            context['clearance_level'] = 3
        else:
            context['clearance_level'] = 2
            
        # Session expiry calculation
        try:
            expiry_date = request.session.get_expiry_date()
            now = timezone.now()
            # If session expires in the past or doesn't have a valid date, default to 30 mins
            if expiry_date < now:
                remaining_seconds = 1800 
            else:
                remaining_seconds = int((expiry_date - now).total_seconds())
        except Exception:
            remaining_seconds = 1800 # default 30 mins

        context['session_expiry_seconds'] = remaining_seconds
        context['officer_id'] = f"TRN-{request.user.id:04d}"
        context['device_is_new'] = request.session.get('device_is_new', False)
        
    return context
