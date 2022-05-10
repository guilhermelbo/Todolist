from django.db import models
from users.models import User

# Create your models here.
class Task(models.Model):
    description = models.CharField(max_length=500)
    completed = models.BooleanField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.description