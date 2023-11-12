from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ph_no = models.CharField(max_length=10)
    address = models.CharField(max_length=400)

    def __str__(self):
        return self.username
