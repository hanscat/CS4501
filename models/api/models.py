
from django.db import models

# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    user_name = models.CharField(max_length=30, unique = True)
    password = models.CharField(max_length=30)

    class Meta:
        abstract = True

class car(models.Model):
    car_color = models.CharField(max_length=30)
    car_make = models.CharField(max_length=30)
    car_model = models.CharField(max_length=10)
    car_year = models.IntegerField(default = 0)
    car_body_type = models.CharField(max_length= 10)
    car_new = models.BooleanField(default=False)
    description = models.CharField(max_length=1000)
    price = models.IntegerField(default=0)

    class Meta:
        abstract = True

class car_to_sell(car):
    price_to_sell = models.IntegerField(default=0)
    warranty = models.BooleanField(default=False)

class car_to_buy(car):
    price_to_offer = models.IntegerField(default=0)

class buyer(user):
    favourite = models.ManyToManyField(car_to_buy, blank = True)

class seller(user):
    car_sell = models.ManyToManyField(car_to_sell, blank = True)


# class inventory(models.Model):
#     owner = models.CharField(max_length=20)
#     num = models.IntegerField(default=0)
#     location = models.CharField(max_length = 20)

# class favorite(models.Model):
#     user = models.CharField(max_length=20)
