from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Complaint(models.Model):
    STATUS = [
        ('pending','Pending'),
        ('in_progress','In Progress'),
        ('resolved','Resolved')
    ]
    CATEGORY = [
        ('maintenance','Maintenance'),
        ('cleanliness','Cleanliness'),
        ('food','Food'),
        ('security','Security'),
        ('other','Other')
    ]
    student     = models.ForeignKey(User, on_delete=models.CASCADE)
    title       = models.CharField(max_length=150)
    category    = models.CharField(max_length=30, choices=CATEGORY)
    description = models.TextField()
    status      = models.CharField(max_length=20, choices=STATUS, default='pending')
    admin_reply = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student.username} - {self.status}"
# Create your models here.
