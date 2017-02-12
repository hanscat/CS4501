
from django.db import models

# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    
    class Meta:
        abstract = True

class buyer(user):
    car_want = models.CharField(max_length=1)


class seller(user):
    car_sell = models.CharField(max_length=1)

class car(models.Model):
    VIN = models.AutoField(primary_key=True)
    car_color = models.CharField(max_length=30)
    car_brand = models.CharField(max_length=30)
    car_model = models.CharField(max_length=10)
    description = models.CharField(max_length=1000)
    price = models.IntegerField(default=0)
    
    class Meta:
        abstract = True

class car_to_sell(car):
    price_to_sell = models.IntegerField(default=0)

class car_to_buy(car):
    price_to_offer = models.IntegerField(default=0)

class inventory(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.CharField(max_length=20)
    num = models.IntegerField(default=0)
    location = models.CharField(max_length = 20)

class favorite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=20)