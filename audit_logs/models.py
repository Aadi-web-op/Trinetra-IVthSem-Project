from django.db import models
from django.conf import settings

class ImmutableLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('FAIL', 'Login Failure'),
        ('BREACH', 'Security Breach'),
    ]

    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        if self.pk:
            # Prevent updates to existing logs
            raise Exception("ImmutableLog cannot be modified")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} by {self.actor} at {self.timestamp}"
