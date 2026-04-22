from django.db import models
from django.conf import settings

class OfficerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    badge_number = models.CharField(max_length=50, unique=True)
    # Using string reference to avoid circular imports and dependency issues
    station = models.ForeignKey('access_control.AllowedStation', on_delete=models.SET_NULL, null=True, blank=True)
    is_biometric_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Officer: {self.badge_number}"

class BiometricDevice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='biometric_devices')
    credential_id = models.CharField(max_length=255, unique=True)
    public_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Device {self.name} for {self.user.username}"
