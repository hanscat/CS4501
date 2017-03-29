from django.conf.urls import url
from . import views

car = [
    url(r'^api/v1/democars/(?P<lb>[0-9]+)to(?P<ub>[0-9]+)', views.demoCars),
    url(r'^api/v1/showCarsColor=/(?P<color>[a-zA-Z]+)', views.showCertainColorCar),
    url(r'^api/v1/showCarsMake=/(?P<make>[a-zA-Z]+)', views.showCertainMakeCar),
    url(r'^api/v1/car/(?P<car_id>[0-9]+)', views.individualCarData, name='carPage'),
    url(r'^api/v1/createCar/$', views.createListing, name='createCarPage'),
]

user = [
    url(r'^api/v1/demousers/(?P<lb>[0-9]+)to(?P<ub>[0-9]+)', views.demoUsers),
    url(r'^api/v1/allbuyers', views.showBuyers),
    url(r'^api/v1/allsellers', views.showSellers),
    url(r'^api/v1/user/(?P<user_id>[0-9]+)', views.individualUserData, name='userPage'),
    url(r'^api/v1/signup/$', views.createUser, name='createUserPage'),
]

auth = [
    url(r'^api/v1/auth/login/', views.login, name='loginPage'),
    url(r'^api/v1/auth/logout/', views.logout, name='logoutPage'),
    url(r'^api/v1/auth/check_status/', views.check_loggedIn, name='check_statusPage'),
]

index = [
    url('', views.invalidURL),
    url(r'^api/v1/login)', views.login, name='login'),
    url(r'^api/v1/logout)', views.logout, name='logout'),
]

urlpatterns =  user + car + auth + index
