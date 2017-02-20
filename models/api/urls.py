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

car = [
       url(r'v1/detail/car/(?P<car_id>[0-9]+)', CarView.as_view()),
    #    url(r'v1/detail/buy_car/(?P<car_id>[0-9]+)', CarBuyView.as_view()),
       url(r'v1/detail/user/(?P<user_id>[0-9]+)', UserView.as_view()),
    #    url(r'v1/detail/buyer/(?P<user_id>[0-9]+)', BuyerView.as_view()),
       url(r'v1/delete/car/(?P<car_id>[0-9]+)', DeleteCarView.as_view()),
    #    url(r'v1/delete/buy_car/(?P<car_id>[0-9]+)', DeleteBuyCarView.as_view()),
       url(r'v1/delete/user/(?P<user_id>[0-9]+)', DeleteUserView.as_view()),
    #    url(r'v1/delete/buyer/(?P<user_id>[0-9]+)', DeleteBuyerView.as_view()),
       ]

urlpatterns = index + car
