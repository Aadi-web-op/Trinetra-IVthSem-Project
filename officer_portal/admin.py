from django.contrib import admin
from .models import ChatMessage, AIUsageLog, LegalDraft

@admin.register(AIUsageLog)
class AIUsageLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'complaint_no', 'timestamp', 'session_id')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'complaint_no', 'justification')
    readonly_fields = ('timestamp',)

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'has_attachment', 'query_preview')
    list_filter = ('timestamp', 'user')
    search_fields = ('user__username', 'query', 'response')
    readonly_fields = ('user', 'query', 'response', 'timestamp', 'file_attachment')
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)
    list_per_page = 20

    fieldsets = (
        ('Officer Details', {
            'fields': ('user', 'timestamp')
        }),
        ('Neural Interaction', {
            'fields': ('query', 'response', 'file_attachment'),
            'classes': ('wide', 'extrapretty'),
        }),
    )

    def query_preview(self, obj):
        return obj.query[:50] + "..." if len(obj.query) > 50 else obj.query
    query_preview.short_description = "Query"

    def has_attachment(self, obj):
        return bool(obj.file_attachment)
    has_attachment.boolean = True
    has_attachment.short_description = "File?"

    def has_delete_permission(self, request, obj=None):
        # REGULATIONS: Officer History cannot be deleted.
        # Only Superusers can delete if absolutely necessary (or completely disable).
        if request.user.is_superuser:
            return True # Or False if you want to be strict
        return False
