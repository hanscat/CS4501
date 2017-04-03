from django.forms import ModelForm
from .models import *
from django.contrib.auth import hashers

class CarForm(ModelForm) :
    class Meta:
        model = car
        fields = '__all__'

class UserForm(ModelForm) :
    class Meta:
        model = user
        fields = '__all__'

    def clean_password(self):
        pw = self.cleaned_data['password']
        if (len(pw) <= 50):
            pw = hashers.make_password(pw)
        return pw


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
