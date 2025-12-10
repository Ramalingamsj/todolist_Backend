from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class List(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    description=models.TextField()
    created_date=models.DateField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
     def __str__(self):
        return f"{self.title} ({self.user.username})"
