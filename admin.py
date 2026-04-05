from django.contrib import admin
from .models import AllowedStation, TrapLog

@admin.register(AllowedStation)
class AllowedStationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'static_ip', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('station_name', 'static_ip')

@admin.register(TrapLog)
class TrapLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'attempted_username', 'timestamp')
    list_filter = ('timestamp',)
    readonly_fields = ('ip_address', 'attempted_username', 'timestamp', 'user_agent')

    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False