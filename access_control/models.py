from django.db import models

class AllowedStation(models.Model):
    station_name = models.CharField(max_length=100)
    static_ip = models.GenericIPAddressField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.station_name} ({self.static_ip})"

class TrapLog(models.Model):
    ip_address = models.GenericIPAddressField()
    attempted_username = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Trap: {self.ip_address} - {self.timestamp}"

class BannedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    banned_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, default="Honeypot Triggered")

    def __str__(self):
        return f"Banned: {self.ip_address} ({self.reason})"
