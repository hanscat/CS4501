from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from .models import *
# Create your views here.

def _success(data_dict, model_name, code):
    correct = { 'status_code' : code, model_name : data_dict }
    return JsonResponse(correct)

def _failure(code, error_msg=''):
    if error_msg == '':
        error = { 'status_code' : code }
    else:
        error = { 'status_code' : code, 'error_message' : error_msg }
    return JsonResponse(error)

def index(request):
    return HttpResponse("Welcome to API page.")

def car_sale(request, car_id):
    try:
        car = car_to_sell.objects.get(pk = car_id)
    except ObjectDoesNotExist:
        return _failure(404, 'Corresponding Car not found')

    if request.method == 'GET':
        car_want = model_to_dict(car)
        return _success(car_want, 'car_to_sale', 200)

    else :
        return_failure(404, 'POST Method not implemented for car')


def car_buy(request, car_id):
    try:
        car = car_to_buy.objects.get(pk = car_id)
    except ObjectDoesNotExist:
        return _failure(404, 'Corresponding Car not found')

    if request.method == 'GET':
        car_want = model_to_dict(car)
        return _success(car_want, 'car_to_buy', 200)

    else :
        return_failure(404, 'POST Method not implemented for car')

def buyer(request, user_id):
    return HttpResponse("Implementing")

def seller(request, user_id):
    return HttpResponse("Implementing")
