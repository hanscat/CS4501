from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.views.generic import View, UpdateView, DeleteView
from .models import *
from .forms import *
from django.db.models import Model
from django.forms import ModelForm

import json
# Create your views here.

# def get_object_or_404(klass, id):
#     queryset = klass.objects.all()
#     try:
#         return queryset.get(pk = id)
#     except ObjectDoesNotExist:
#         raise _failure(404, klass.__name__ + "with given id doesn't exists")

def get_success(code, data_dict, model_name):
    correct = {"Status Code" : code, model_name : data_dict }
    return JsonResponse(correct)

def _success(code, message):
    correct = {"Status Code" : code, "message" : message}
    return JsonResponse(correct)

def _failure(code, message):
    failure = {"Status Code" : code, "message" : message}
    return JsonResponse(failure)

def index(request):
    greeting = "Welcome to API page."
    return HttpResponse(greeting)

class CarView(View):
    model = Model
    modelForm = ModelForm

    def get(self, request, *args, **kwargs):
        # car = get_object_or_404(self.model, pk = kwargs['car_id'])
        try :
            car = self.model.objects.get(pk = kwargs['car_id'])
        except ObjectDoesNotExist:
            return _failure(404, "Car doesn't exist")

        car = model_to_dict(car)
        return get_success('200', car, self.model.__name__)

    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        data_dict = json.loads(data)
        form = self.modelForm(data_dict)
        if form.is_valid() :
            if int(kwargs['car_id']) in self.model.objects.values_list('pk', flat = True) :
                return self.update(kwargs['car_id'], data_dict)
            else:
                form.save()
                return _success(201, 'Create Success')
        else :
            return _failure(400, 'form invalid, bad post request.')

    def update(self, car_id, data_dict):
        car = self.model.objects.get(pk = car_id)
        form = self.modelForm(data_dict, instance = car)
        form.save()
        return  _success(202, 'Update Success')

class UserView(View):
    model = Model
    submodel = Model
    modelForm = ModelForm

    def get(self, request, *args, **kwargs):
        try :
            user = self.model.objects.get(pk = kwargs['user_id'])
        except ObjectDoesNotExist:
            return _failure(404, "User doesn't exist")
        user_want = model_to_dict(user)
        l = []
        if 'favourite' in [f.name for f in self.model._meta.get_fields()]:
            for car in user_want['favourite'] :
                l.append(car.pk)
            user_want['favourite'] = l

        elif "car_sell" in [f.name for f in self.model._meta.get_fields()]:
            for car in user_want['car_sell'] :
                l.append(car.pk)
            user_want['car_sell'] = l

        return get_success(200, user_want, self.model.__name__)

    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        data_dict = json.loads(data)
        l = set()
        if 'car_sell' in data_dict.keys():
            if self.model != seller :
                return _failure(400, 'form invalid, bad post request.')
            for i in data_dict['car_sell']:
                try :
                    obj = self.submodel.objects.get(pk=i)
                except ObjectDoesNotExist:
                    return _failure(404, 'requested car_sell list not valid (no such car in db)')
                l.add(obj)
            data_dict['car_sell'] = l

        elif 'favourite' in data_dict.keys():
            if self.model != buyer :
                return _failure(400, 'form invalid, bad post request.')
            this = buyer
            for i in data_dict['favourite']:
                try :
                    obj = self.submodel.objects.get(pk=i)
                except ObjectDoesNotExist:
                    return _failure(404, 'requested favourite list not valid (no such car in db)')
                l.add(obj)
            data_dict['favourite'] = l
            # data_dict['car_sell'] = [self.submodel.objects.get(pk = i) for i in data_dict['car_sell']]

        if int(kwargs['user_id']) in self.model.objects.values_list('pk', flat = True) :
            return self.update(kwargs['user_id'], data_dict)
        form = self.modelForm(data_dict)
        if form.is_valid():
            form.save()
            return _success(201, 'Create Success')
        else:
            return _failure(400, 'form invalid, bad post request.')

    def update(self, user_id, data_dict):
        user = self.model.objects.get(pk = user_id)
        form = self.modelForm(data_dict, instance = user)

        if form.is_valid():
            form.save()
            return _success(202, 'Update Success')
        else :
            return _failure(400, 'form invalid, bad post request.')


class DeleteCarView(DeleteView):
    model = Model
    owner = Model

    def delete(self, request, *args, **kwargs) :
        try :
            car = self.model.objects.get(pk = kwargs['car_id'])
        except ObjectDoesNotExist:
            return _failure(404, "Car doesn't exist")
        self.Userdelete(car)
        car.delete()
        return _success(202, 'Delete Success')

    def Userdelete(self, car) :
        for user in self.owner.objects.all():
            if 'car_sell' in [f.name for f in self.model._meta.get_fields()]:
                if car in user.car_sell.all():
                    user.car_sell.remove(car)

            elif 'favourite' in [f.name for f in self.model._meta.get_fields()]:
                if car in user.favourite.all():
                    user.car_sell.remove(car)

class DeleteUserView(DeleteView):
    model = Model

    def delete(self, request, *args, **kwargs) :
        try :
            user = self.model.objects.get(pk = kwargs['user_id'])
        except ObjectDoesNotExist:
            return _failure(404, "User doesn't exist")
        user.delete()
        return _success(202, 'Delete Success')



class DeleteSellCarView(DeleteCarView):
    model = car_to_sell
    owner = seller

class DeleteBuyCarView(DeleteCarView):
    model = car_to_buy
    owner = buyer

class DeleteSellerView(DeleteUserView):
    model = seller

class DeleteBuyerView(DeleteUserView):
    model = buyer

class BuyerView(UserView):
    model = buyer
    modelForm = BuyerForm
    submodel = car_to_buy

class SellerView(UserView):
    model = seller
    modelForm = SellerForm
    submodel = car_to_sell

class CarSellView(CarView):
    model = car_to_sell
    modelForm = CarSellForm

class CarBuyView(CarView):
    model = car_to_buy
    modelForm = CarBuyForm

# class CarSellView(View):
#     model = car_to_sell
#
#     def get(self, request, *args, **kwargs):
#         car = get_object_or_404(car_to_sell, pk=kwargs['car_id'])
#         car = model_to_dict(car)
#         return _success(car, 'car_to_sell')
#
#     def post(self, request, *args, **kwargs):
#         data = request.body.decode('utf-8')
#         data_dict = json.loads(data)
#         form = CarSellForm(data_dict)
#         if form.is_valid() :
#             form.save()
#             return HttpResponse('Success')
#         else :
#             return HttpResponse('Bad Post Request')
#
#
# class CarBuyView(View):
#     model = car_to_buy
#
#     def get(self, request, *args, **kwargs):
#         car= get_object_or_404(car_to_buy, pk=kwargs['car_id'])
#         car = model_to_dict(car)
#         return _success(car, 'car_to_buy')
#
#     def post(self, request, *args, **kwargs):
#         data = request.body.decode('utf-8')
#         data_dict = json.loads(data)
#         form = CarBuyForm(data_dict)
#         if form.is_valid() :
#             form.save()
#             return HttpResponse('Success')
#         else :
#             return HttpResponse('Bad Post Request')


# class BuyerView(View):
#     model = buyer
#
#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(buyer, pk=kwargs['user_id'])
#         user_want = model_to_dict(user)
#         l = []
#         for car in user['favourite'] :
#             l.append(car.pk)
#         user['favourite'] = l;
#         return _success(user_want, 'buyer')
#
#     def post(self, request, *args, **kwargs):
#         data = request.body.decode('utf-8')
#         data_dict = json.loads(data)
#         form = BuyerForm(data_dict)
#         if form.is_valid() :
#             form.save()
#             return HttpResponse('Success')
#         else :
#             return HttpResponse('Bad Post Request')
#
# class SellerView(View):
#     model = seller
#
#     def get(self, request, *args, **kwargs):
#         user = get_object_or_404(seller, pk=kwargs['user_id'])
#         user = model_to_dict(user)
#         l = []
#         for car in user['car_sell'] :
#             l.append(car.pk)
#         user['car_sell'] = l;
#         return _success(user, 'seller')
#
#     def post(self, request, *args, **kwargs):
#         data = request.body.decode('utf-8')
#         data_dict = json.loads(data)
#         form = SellerForm(data_dict)
#         if form.is_valid() :
#             form.save()
#             return HttpResponse('Success')
#         else :
#             return HttpResponse('Bad Post Request')




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
