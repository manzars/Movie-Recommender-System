from django.db import models

# Create your models here.
class User(models.Model):
    Name = models.CharField(max_length=120)
    user_name = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)
    country = models.CharField(max_length=120)
    phone = models.CharField(max_length=120)


class Admin(models.Model):
    Name = models.CharField(max_length=120)
    user_name = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    email = models.EmailField(max_length=50)