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
from . import views, auth_view
from .views import *
from .auth_view import *

index = [url(r'^$', views.index),]

car = [
       url(r'v1/detail/car/(?P<car_id>[0-9]+)', CarView.as_view()),
       url(r'v1/detail/car/', views.SearchCar, name='SearchCar'),
       url(r'v1/delete/car/(?P<car_id>[0-9]+)', DeleteCarView.as_view()),
       ]

user = [
        url(r'v1/detail/user/(?P<user_id>[0-9]+)', UserView.as_view()),
        url(r'v1/detail/user/', views.SearchUser, name='SearchUser'),
        url(r'v1/delete/user/(?P<user_id>[0-9]+)', DeleteUserView.as_view()),
]

auth = [
        url(r'v1/auth/login/', auth_view.login, name='login'),
        url(r'v1/auth/logout/', auth_view.logout, name='login'),
        url(r'v1/auth/check_status/', auth_view.check_status, name='login'),

]

urlpatterns = index + car + auth + user
