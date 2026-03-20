from django.db import models
from django.contrib.auth.models import User

class StudentProfile(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number  = models.CharField(max_length=20)
    phone        = models.CharField(max_length=15, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    course       = models.CharField(max_length=100, blank=True)
    year         = models.IntegerField(default=1)
    warden       = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='assigned_students'
    )

    def __str__(self):
        return f"{self.user.username} - Room {self.room_number}"