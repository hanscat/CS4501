from django.conf.urls import url
from . import views

car = [
    # url(r'^api/v1/democars/(?P<lb>[0-9]+)to(?P<ub>[0-9]+)', views.demoCars),
    # url(r'^api/v1/showCarsColor=/(?P<color>[a-zA-Z]+)', views.showCertainColorCar),
    # url(r'^api/v1/showCarsMake=/(?P<make>[a-zA-Z]+)', views.showCertainMakeCar),
    url(r'^api/v1/car/(?P<car_id>[0-9]+)', views.car_detail, name='carPage'),
    url(r'^api/v1/createCar/$', views.create_car, name='createCarPage'),
]

user = [
    # url(r'^api/v1/demousers/(?P<lb>[0-9]+)to(?P<ub>[0-9]+)', views.demoUsers),
    # url(r'^api/v1/allbuyers', views.showBuyers),
    # url(r'^api/v1/allsellers', views.showSellers),
    url(r'^api/v1/user/(?P<user_id>[0-9]+)', views.user_detail, name='userPage'),
    url(r'^api/v1/user/signup/$', views.create_user, name='createUserPage'),
    url(r'^api/v1/user/update/', views.update_user, name='updateUser'),
    url(r'^api/v1/user/concise/(?P<user_id>[0-9]+)', views.concise_user_detail, name='speicalUserPage')
]

auth = [
    url(r'^api/v1/auth/login/', views.login, name='loginPage'),
    url(r'^api/v1/auth/logout/', views.logout, name='logoutPage'),
    url(r'^api/v1/auth/check_status/', views.check_loggedIn, name='check_statusPage'),
]

index = [
    # url('', views.invalidURL),
    url(r'^api/v1/home/', views.home, name='home'),
]

urlpatterns =  user + car + auth + index
