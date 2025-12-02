from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    address = models.TextField(blank=True, help_text="Physical address for verification")
    phone_number = models.CharField(max_length=20, blank=True, help_text="Contact number for coordination")

    def __str__(self):
        return self.username
