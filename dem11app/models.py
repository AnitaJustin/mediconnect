from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ph_no = models.CharField(max_length=10)
    address = models.CharField(max_length=400)

    def __str__(self):
        return self.username

class medicines(models.Model):
    name = models.CharField(max_length=256)
    dosage=models.CharField(max_length=50)
    disease=models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expirydate=models.DateField()
    contents=models.CharField(max_length=250)
    manufacturer=models.CharField(max_length=80)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class OtherAids(models.Model):
    name = models.CharField(max_length=256)
    age=models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=3)
    manufacturer=models.CharField(max_length=80)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    

class receiver(models.Model):
    medicine=models.CharField(max_length=250)
    quantity=models.PositiveIntegerField()
    disease=models.CharField(max_length=150)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prescription_photo = models.ImageField(upload_to='prescriptions/', null=True, blank=True)
    def __str__(self):
        return self.medicine
    


