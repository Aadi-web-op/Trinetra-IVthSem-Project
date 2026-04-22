from django.contrib import admin
from .models import OfficerProfile, BiometricDevice

@admin.register(OfficerProfile)
class OfficerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge_number', 'station', 'is_biometric_enabled')
    search_fields = ('user__username', 'badge_number')

@admin.register(BiometricDevice)
class BiometricDeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    readonly_fields = ('credential_id', 'public_key', 'created_at')
