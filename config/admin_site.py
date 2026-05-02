"""
TRINETRA Custom Admin Site
Provides real-time system telemetry to the admin dashboard index.
"""
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model


from django.contrib import admin
from django.contrib.auth import get_user_model

# Override the default admin site headers
admin.site.site_header = 'TRINETRA COMMAND'
admin.site.site_title = 'Trinetra Command Center'
admin.site.index_title = 'System Operations'

# Keep a reference to the original each_context
_original_each_context = admin.site.each_context

def custom_each_context(request):
    """Inject real-time system stats into every admin page context."""
    context = _original_each_context(request)

    try:
        User = get_user_model()
        from officer_portal.models import Case, Evidence, ChatMessage, AITask
        from access_control.models import TrapLog, BannedIP, AllowedStation
        from audit_logs.models import ImmutableLog

        context['stat_users'] = User.objects.filter(is_staff=True).count()
        context['stat_stations'] = AllowedStation.objects.filter(is_active=True).count()
        context['stat_cases'] = Case.objects.count()
        context['stat_evidence'] = Evidence.objects.count()
        context['stat_chats'] = ChatMessage.objects.count()
        context['stat_threats'] = TrapLog.objects.count()
        context['stat_banned'] = BannedIP.objects.count()
        context['stat_logs'] = ImmutableLog.objects.count()
        context['stat_active_tasks'] = AITask.objects.filter(status='pending').count()
        context['stat_open_cases'] = Case.objects.filter(status='OPEN').count()
        context['stat_high_priority'] = Case.objects.filter(priority='HIGH', status='OPEN').count()
    except Exception:
        # Fallback if models aren't migrated yet
        context.setdefault('stat_users', 0)
        context.setdefault('stat_stations', 0)
        context.setdefault('stat_cases', 0)
        context.setdefault('stat_evidence', 0)
        context.setdefault('stat_chats', 0)
        context.setdefault('stat_threats', 0)
        context.setdefault('stat_banned', 0)
        context.setdefault('stat_logs', 0)
        context.setdefault('stat_active_tasks', 0)
        context.setdefault('stat_open_cases', 0)
        context.setdefault('stat_high_priority', 0)

    return context

# Apply the monkey patch
admin.site.each_context = custom_each_context

# For compatibility with urls.py
trinetra_admin = admin.site

