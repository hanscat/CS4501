"""HelloWorld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
from .views import *

index = [url(r'^$', views.index),]
car = [url(r'detail/sale_car/(?P<car_id>[0-9]+)', CarSellView.as_view()),
       url(r'detail/buy_car/(?P<car_id>[0-9]+)', CarBuyView.as_view()),
       url(r'detail/seller/(?P<user_id>[0-9]+)', SellerView.as_view()),
       url(r'detail/buyer/(?P<user_id>[0-9]+)', BuyerView.as_view()),
       url(r'create/user/seller', SellerView.as_view()),
       url(r'create/user/buyer', BuyerView.as_view()),
       url(r'update/user/seller/(?P<user_id>[0-9]+)', SellerView.update()),
       url(r'update/user/buyer/(?P<user_id>[0-9]+)', BuerView.update()),
       ]

urlpatterns = index + car
