from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Notice(models.Model):
    PRIORITY = [
        ('normal','Normal'),
        ('important','Important'),
        ('urgent','Urgent')
    ]
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    priority   = models.CharField(max_length=20, choices=PRIORITY, default='normal')
    posted_by  = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at  = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField(blank=True, null=True)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return f"[{self.priority}] {self.title}"
# Create your models here.
