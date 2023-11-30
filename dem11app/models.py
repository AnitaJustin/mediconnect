from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ph_no = models.CharField(max_length=10)
    address = models.CharField(max_length=400)

    def __str__(self):
        return self.username
class Admin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128) 
    email=models.EmailField() 

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
    approved=models.BooleanField(default="False")
    removed=models.BooleanField(default="False")
    reached_store=models.BooleanField(default="False")
    def __str__(self):
        return self.name


class OtherAids(models.Model):
    name = models.CharField(max_length=256)
    age=models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=3)
    manufacturer=models.CharField(max_length=80)
    current_photo = models.ImageField(upload_to='media/otheraids/', null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approved=models.BooleanField(default="False")
    removed=models.BooleanField(default="False")
    reached_store=models.BooleanField(default="False")

    def __str__(self):
        return self.name
    

class req_med(models.Model):
    medicine=models.CharField(max_length=250)
    quantity=models.PositiveIntegerField()
    disease=models.CharField(max_length=150)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    prescription_photo = models.ImageField(upload_to='media/prescriptions/', null=True, blank=True)
    approved=models.BooleanField(default="False")
    removed=models.BooleanField(default="False")  
    collected=models.BooleanField(default="False")
    def __str__(self):
        return self.medicine
    


class saving_request(models.Model):
    aid = models.ForeignKey(OtherAids, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    approved=models.BooleanField(default="False")
    removed=models.BooleanField(default="False")
    collected=models.BooleanField(default="False")


class Payments(models.Model):
    name=models.CharField(max_length=150)
    amount = models.FloatField()
    mail=models.EmailField()
    payment_id=models.CharField(max_length=150)
    paid=models.BooleanField(default=False)
