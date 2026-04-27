from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('conductor', 'Conductor'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.username
