
from django.db import models

# Create your models here.
class car(models.Model):
    car_color = models.CharField(max_length=30, default="")
    car_make = models.CharField(max_length=30, default="")
    car_model = models.CharField(max_length=10, default="")
    car_year = models.IntegerField(default = 0)
    car_body_type = models.CharField(max_length= 10, default="")
    car_new = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, default="This is a car")
    price = models.IntegerField(default=0)
    class Meta:
        managed = True


class user(models.Model):
    first_name = models.CharField(max_length=20, default="new")
    last_name  = models.CharField(max_length=20, default="user")
    user_name = models.CharField(max_length=30, unique = True, default="newUser")
    password = models.CharField(max_length=30, default="password")
    favourite = models.ManyToManyField(car, blank = True, related_name = "like")
    car_sell = models.ManyToManyField(car, blank = True, related_name = "owner")
    class Meta:
        managed = True



# class inventory(models.Model):
#     owner = models.CharField(max_length=20)
#     num = models.IntegerField(default=0)
#     location = models.CharField(max_length = 20)

# class favorite(models.Model):
#     user = models.CharField(max_length=20)
