from django.db import models
from django.contrib.auth.models import User

class EmergencyContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=50)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class MedicalReport(models.Model):
    REPORT_TYPES = [
        ('pdf', 'PDF Report'),
        ('image', 'Image Report'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
    file = models.FileField(upload_to='medical_reports/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username if self.user else 'Anonymous'}"

class ReportAnalysis(models.Model):
    report = models.OneToOneField(MedicalReport, on_delete=models.CASCADE)
    analysis_text = models.TextField()
    health_tips = models.TextField()
    yoga_suggestions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for {self.report.title}"

class EmergencyAlert(models.Model):
    ALERT_TYPES = [
        ('ambulance', 'Ambulance Call'),
        ('family', 'Family Alert'),
        ('location', 'Location Share'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.alert_type} - {self.created_at}" 