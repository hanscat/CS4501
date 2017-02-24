from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^api/v1/homepage/(?P<user_id>[0-9]+)/?', views.individualUserData, name = 'userPage'),
        url(r'^api/v1/carpage/(?P<car_id>[0-9]+)/?', views.individualCarData, name = 'carPage'),
        url ('', views.invalidURL),
        ]