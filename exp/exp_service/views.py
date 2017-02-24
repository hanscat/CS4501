from django.shortcuts import render
from django.shortcuts import render
import urllib.request, json
from django.http import JsonResponse


# Create your views here.
modelsAPI = "http://localhost:8001/api/v1/"

def invalidURL(request):
    err = {}
    err['message'] = "Oops, you just entered an invalid API request!"
    err['status'] = False
    return JsonResponse(err)

#def individualUserData(request):

def individualCarData(pk, request):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/car/"
        requester = urllib.request.Request(urlForParticularCar + pk)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        car = json.loads(response)
    return JsonResponse(car)


def individualUserData(pk, request):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/user/"
        requester = urllib.request.Request(urlForParticularCar + pk)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        user = json.loads(response)
    return JsonResponse(user)

