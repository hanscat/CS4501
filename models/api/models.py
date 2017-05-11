from django.db import models

# Create your models here.
class car(models.Model):
    car_color = models.CharField(max_length=30, default="")
    car_make = models.CharField(max_length=30, default="")
    car_model = models.CharField(max_length=10, default="")
    car_year = models.IntegerField(default=0)
    car_body_type = models.CharField(max_length=10, default="")
    car_new = models.BooleanField(default=False)
    description = models.CharField(max_length=1000, default="This is a car")
    price = models.IntegerField(default=0)
    class Meta:
        managed = True


class user(models.Model):
    first_name = models.CharField(max_length=20, default="new")
    last_name = models.CharField(max_length=20, default="user")
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=100, default="password")
    favourite = models.ManyToManyField(car, blank=True, related_name="like")
    car_sell = models.ManyToManyField(car, blank=True, related_name="owner")
    class Meta:
        managed = True

class Authenticator(models.Model):
    userid = models.IntegerField(default=0)
    auth = models.CharField(max_length=100, primary_key=True, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

class recommendation(models.Model):
    item = models.OneToOneField(car, on_delete=models.CASCADE, related_name = "idForCar")
    rec = models.ManyToManyField(car, blank = True, related_name = "recommend")
# class inventory(models.Model):
#     owner = models.CharField(max_length=20)
#     num = models.IntegerField(default=0)
#     location = models.CharField(max_length = 20)

# class favorite(models.Model):
#     user = models.CharField(max_length=20)
class Recommendation(models.Model):
    item_id = models.CharField(max_length=5, primary_key=True)
    recommended_list = models.CharField(
        max_length=250)  # Comma-separated list of item_ids that were co-viewed 3+ times

    def as_json(self):
        return dict(
            curr_item_id=self.item_id,
            curr_recommended_items=self.recommended_items
        )
