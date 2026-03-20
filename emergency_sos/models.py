from django.db import models
from django.contrib.auth.models import User

class SOSAlert(models.Model):
    STATUS = [
        ('sent',         'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('resolved',     'Resolved')
    ]
    student     = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='sos_alerts'
    )
    warden      = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='received_sos_alerts'
    )
    message     = models.TextField(default='Emergency! Please help.')
    location    = models.CharField(max_length=200, blank=True)
    status      = models.CharField(max_length=20, choices=STATUS, default='sent')
    sent_at     = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"SOS - {self.student.username} - {self.sent_at}"