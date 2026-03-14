from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    PRIORITY_CHOICES =[
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    order = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.title

# Create your models here.
