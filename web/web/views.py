from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request, json


expApi = 'http://exp-api:8000/api/v1/'
def index(request):
    template = loader.get_template('home.html')
    url = expApi + "democars/1to8"
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    cars = json.loads(response)
    if cars["status_code"] == 200 :
        cars = cars["cars"]
        return render(request, 'home.html', {'cars': cars})
    else :
        return bad_request(request)

def user_detail(request, user_id):
    template = loader.get_template('home.html')
    url = expApi + "car/" + str(user_id)
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    car = json.loads(response)
    if car["status_code"] == 200 :
        car = [car["car"]]
        return render(request, 'home.html', {'cars': car})
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
