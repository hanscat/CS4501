from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.views.generic import ListView
from .models import *
from .forms import *

import json
# Create your views here.

def _success(data_dict, model_name, code):
    correct = { 'status_code' : code, model_name : data_dict }
    return JsonResponse(correct)

def index(request):
    return HttpResponse("Welcome to API page.")

class CarSellView(ListView):
    model = car_to_sell

    def get(self, request, *args, **kwargs):
        car = get_object_or_404(car_to_sell, pk=kwargs['car_id'])
        car = model_to_dict(car)
        return _success(car, 'car_to_sell', 200)

    def post(self, request, *args, **kwargs):
        def post(self, request, *args, **kwargs):
            data = request.body.decode('utf-8')
            data_dict = json.loads(data)
            form = CarSellForm(data_dict)
            if form.is_valid() :
                form.save()
                return HttpResponse('Success')
            else :
                return HttpResponse('Bad Post Request')


class CarBuyView(ListView):
    model = car_to_buy

    def get(self, request, *args, **kwargs):
        car= get_object_or_404(car_to_buy, pk=kwargs['car_id'])
        car = model_to_dict(car)
        return _success(car, 'car_to_buy', 200)

    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        data_dict = json.loads(data)
        form = CarBuyForm(data_dict)
        if form.is_valid() :
            form.save()
            return HttpResponse('Success')
        else :
            return HttpResponse('Bad Post Request')



class BuyerView(ListView):
    model = buyer

    def get(self, request, *args, **kwargs):
        user= get_object_or_404(buyer, pk=kwargs['user_id'])
        user_want = model_to_dict(user)
        return _success(user_want, 'buyer', 200)

    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        data_dict = json.loads(data)
        form = BuyerForm(data_dict)
        if form.is_valid() :
            form.save()
            return HttpResponse('Success')
        else :
            return HttpResponse('Bad Post Request')

class SellerView(ListView):
    model = seller

    def get(self, request, *args, **kwargs):
        user= get_object_or_404(seller, pk=kwargs['user_id'])
        user_want = model_to_dict(user)
        return _success(user_want, 'seller', 200)

    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        data_dict = json.loads(data)
        form = SellerForm(data_dict)
        if form.is_valid() :
            form.save()
            return HttpResponse('Success')
        else :
            return HttpResponse('Bad Post Request')

# Original implementation changed to class_based view
# def SellerDetail(request, user_id):
#     user = get_object_or_404(seller, pk=user_id)
#
#     if request.method == 'GET':
#         user_want = model_to_dict(user)
#         return _success(user_want, 'seller', 200)
#     elif request.method == 'POST':
#         return HttpResponse("Implementing")
#     else :
#         return HttpResponse("Method Not Known")
#
# def BuyerDetail(request, user_id):
#     user= get_object_or_404(buyer, pk=user_id)
#
#     if request.method == 'GET':
#         user_want = model_to_dict(user)
#         return _success(user_want, 'buyer', 200)
#     elif request.method == 'POST':
#         return HttpResponse("Implementing")
#     else :
#         return HttpResponse("Method Not Known")
