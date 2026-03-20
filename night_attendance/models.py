from django.db import models
from django.db import models
from django.contrib.auth.models import User

class NightAttendance(models.Model):
    STATUS = [
        ('present','Present'),
        ('absent','Absent'),
        ('on_leave','On Leave')
    ]
    student  = models.ForeignKey(User, on_delete=models.CASCADE)
    date     = models.DateField()
    status   = models.CharField(max_length=20, choices=STATUS, default='present')
    remarks  = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ('student','date')

    def __str__(self):
        return f"{self.student.username} - {self.date} - {self.status}"
# Create your models here.
