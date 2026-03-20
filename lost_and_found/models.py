from django.db import models
from django.db import models
from django.contrib.auth.models import User

class LostFoundItem(models.Model):
    TYPE = [('lost','Lost'),('found','Found')]

    posted_by   = models.ForeignKey(User, on_delete=models.CASCADE)
    item_type   = models.CharField(max_length=10, choices=TYPE)
    title       = models.CharField(max_length=150)
    description = models.TextField()
    location    = models.CharField(max_length=200)
    is_resolved = models.BooleanField(default=False)
    posted_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.item_type}] {self.title} - {self.posted_by.username}"
# Create your models here.
