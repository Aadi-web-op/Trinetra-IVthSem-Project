from django.db import models
from django.conf import settings

class AIUsageLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    complaint_no = models.CharField(max_length=100, help_text="Reference/Complaint Number")
    justification = models.TextField(help_text="Reason for using AI")
    timestamp = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Access: {self.complaint_no} by {self.user.username}"

class LegalDraft(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference_no = models.CharField(max_length=100)
    justification = models.TextField()
    generated_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Draft: {self.reference_no} ({self.timestamp.strftime('%Y-%m-%d')})"

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_history')
    query = models.TextField(help_text="The officer's input query", blank=True)
    response = models.TextField(help_text="The AI's response")
    file_attachment = models.FileField(upload_to='ai_uploads/%Y/%m/', blank=True, null=True)
    case = models.ForeignKey('Case', on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class Case(models.Model):
    case_no = models.CharField(max_length=255, unique=True, help_text="Unique Case ID used by AI")
    suspect_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the suspect/target")
    description = models.TextField(blank=True, null=True, help_text="Detailed description of the incident")
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    
    PRIORITY_CHOICES = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    assigned_officer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cases', null=True, blank=True)
    
    summary = models.TextField(blank=True, null=True, help_text="Running log/summary of the case")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cases' # Explicitly set table name to match AI requirement
        managed = True     # Let Django manage migrations

    def __str__(self):
        return f"{self.case_no} - {self.suspect_name or 'Unknown'}"

class Evidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='evidence')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='evidence/%Y/%m/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evidence for {self.case.case_no} by {self.uploaded_by.username}"

class AITask(models.Model):
    """Stores background AI task results so any Gunicorn worker can retrieve them."""
    task_id = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.CharField(max_length=20, default='pending')  # 'pending' or 'done'
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Task {self.task_id[:8]}... [{self.status}]"
