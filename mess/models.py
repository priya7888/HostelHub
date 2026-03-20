from django.db import models
from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    MEAL_CHOICES = [
        ('breakfast','Breakfast'),
        ('lunch','Lunch'),
        ('dinner','Dinner')
    ]
    name      = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    date      = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.meal_type} - {self.date}"

class FoodVote(models.Model):
    student   = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    voted_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student','food_item')

    def __str__(self):
        return f"{self.student.username} voted {self.food_item.name}"
# Create your models here.
