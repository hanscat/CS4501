from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request, json


expApi = 'http://exp-api:8000/api/v1/'
def index(request):
    template = loader.get_template('home.html')
    urlForCar = expApi + "democars/1to8"
    requester = urllib.request.Request(urlForCar)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    cars = json.loads(response)
    urlForUser= expApi + "user/1"
    requester = urllib.request.Request(urlForUser)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    user = json.loads(response)
    if cars["status_code"] == 200 :
        cars = cars["cars"]
        if user["status_code"] == 200:
            user = user["users"]
            user = [user]
        return render(request, 'home.html', {'cars': cars, 'users': user})
    else :
        return bad_request(request)

def user_detail(request, user_id):
    template = loader.get_template('home.html')
    url = expApi + "user/" + str(user_id)
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    user = json.loads(response)
    if user["status_code"] == 200 :
        user = [user["users"]]
        return render(request, 'userdetail.html', {'users': user})
    else :
        return bad_request(request)

def car_detail(request, car_id):
    template = loader.get_template('home.html')
    url = expApi + "car/" + str(car_id)
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    car = json.loads(response)
    if car["status_code"] == 200 :
        car = [car["cars"]]
        return render(request, 'cardetail.html', {'cars': car})
    else :
        return bad_request(request)

def bad_request(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render(request))

def internal_error(request):
    template = loader.get_template('500.html')
    return HttpResponse(template.render(request))
