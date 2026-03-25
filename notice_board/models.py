from django.db import models
from django.contrib.auth.models import User


class Notice(models.Model):
    PRIORITY_CHOICES = [
        ('normal',    'Normal'),
        ('important', 'Important'),
        ('urgent',    'Urgent'),
    ]

    title      = models.CharField(max_length=200)
    content    = models.TextField()
    priority   = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal'
    )
    posted_by  = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notices'
    )
    posted_at  = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField(null=True, blank=True)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted_at']