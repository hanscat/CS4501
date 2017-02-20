from django.forms import ModelForm
from .models import *

class CarForm(ModelForm) :
    class Meta:
        model = car
        fields = '__all__'

class UserForm(ModelForm) :
    class Meta:
        model = user
        fields = '__all__'

# class CarSellForm(ModelForm) :
#     class Meta:
#         model = car_to_sell
#         fields = '__all__'
#
# class CarBuyForm(ModelForm) :
#     class Meta:
#         model = car_to_buy
#         fields = '__all__'
#
# class BuyerForm(ModelForm) :
#     class Meta:
#         model = buyer
#         fields = '__all__'
#
# class SellerForm(ModelForm) :
#     class Meta:
#         model = seller
#         fields = '__all__'
