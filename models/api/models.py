from django.db import models

# Create your models here.
class user(models.Model):
    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    user_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    class Meta:
        abstract = true;

class buyer(user):
    car_want = models.onetomanyField(car_want_buy)

class seller(user):
    car_own = models.onetomanyField(car_to_sell)

class car(models.Model):
    car_color = models.CharField(max_field=30)
    car_brand = models.CharField(max_field=30)
    car_model = models.CharField(max_field=10)
    description = models.CharField(max_field=1000)
    price = models.IntegerField(default=0)

    class Meta:
        abstract = true;

class car_to_sell(car):
    price_to_sell = models.IntegerField(default=0)

class car_want_buy(car):
    price_to_offer = models.IntegerField(default=0)
