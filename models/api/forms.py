from django.forms import ModelForm
from .models import *

class CarSellForm(ModelForm) :

    class Meta:
        model = car_to_sell
        fields = '__all__'

class CarBuyForm(ModelForm) :
    class Meta:
        model = car_to_buy
        fields = '__all__'

class BuyerForm(ModelForm) :
    class Meta:
        model = buyer
        fields = '__all__'


class SellerForm(ModelForm) :
    class Meta:
        model = seller
        fields = '__all__'
