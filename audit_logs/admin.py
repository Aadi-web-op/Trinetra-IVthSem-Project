from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import ImmutableLog

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Exposes Django's internal action log as a strictly immutable administrative record.
    """
    list_display = ('action_time', 'user', 'action_flag', 'object_repr', 'change_message')
    list_filter = ('action_time', 'user', 'action_flag')
    search_fields = ('object_repr', 'change_message')
    date_hierarchy = 'action_time'
    
    # Enforce Immutability (Read-Only)
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
        
    # Disable bulk delete actions
    actions = None

@admin.register(ImmutableLog)
class ImmutableLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'actor', 'ip')
    list_filter = ('action', 'timestamp')
    search_fields = ('ip', 'metadata')
    readonly_fields = ('actor', 'action', 'ip', 'timestamp', 'metadata')
    
    # Enforce Immutability
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
        
    def has_delete_permission(self, request, obj=None):
        return False
        
    actions = None
