from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    register_no = models.CharField(max_length=15, unique=True)
    branch = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    parent_phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} ({self.register_no})"
