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

def get_success(code, data_dict, model_name):
    correct = {"status_code" : code, model_name : data_dict }
    return JsonResponse(correct)

def _success(code, message):
    correct = {"status_code" : code, "message" : message}
    return JsonResponse(correct)

def _failure(code, message):
    failure = {"status_code" : code, "message" : message}
    return JsonResponse(failure)

def index(request):
    greeting = "Welcome to API page."
    return _success(200, greeting)

def SearchCar(request):
    dic = request.GET
    if dic == {} :
        return _failure(404, "invalid URL")
    dic = dict(dic)
    for key in dic.keys():
        if key not in [f.name for f in car._meta.get_fields()] :
            return _failure(404, "invalid fields")
        dic[key] = dic[key][0]
    cars = car.objects.filter(**dic)
    li = []
    for oneCar in cars :
        li.append(model_to_dict(oneCar))
    cars = li
    if len(cars) == 0:
        return _failure(404, "no such cars")
    else :
        return get_success(200, cars, "car")

def SearchUser(request):
    dic = request.GET
    if dic == {} :
        return _failure(404, "invalid URL")
    dic = dict(dic)
    for key in dic.keys():
        if key not in [f.name for f in user._meta.get_fields()]:
            return _failure(404, "invalid fields")
        dic[key] = dic[key][0]
    users = user.objects.filter(**dic)
    li = []
    for oneUser in users :
        user_want = model_to_dict(oneUser)
        fav = []
        if 'favourite' in [f.name for f in user._meta.get_fields()]:
            for car in user_want['favourite'] :
                fav.append(model_to_dict(car))
            user_want['favourite'] = fav

        car_sell = []
        if "car_sell" in [f.name for f in user._meta.get_fields()]:
            for car in user_want['car_sell'] :
                car_sell.append(model_to_dict(car))
            user_want['car_sell'] = car_sell
        li.append(user_want)
    users = li
    return get_success(200, users, "user")

def GetRec(request, car_id):
    if request.method == 'GET' :
        try :
            rec = recommendation.objects.get(item = car_id)
            rec = model_to_dict(rec)
            recs = []
            for car in rec['rec']:
                car = model_to_dict(car)
                recs.append(car)
        except ObjectDoesNotExist:
            recs = []
        return get_success(200, recs, "rec")

class CarView(View):
    model = car
    modelForm = CarForm

    def get(self, request, *args, **kwargs):
        # car = get_object_or_404(self.model, pk = kwargs['car_id'])
        try :
            car = self.model.objects.get(pk = kwargs['car_id'])
        except ObjectDoesNotExist:
            return _failure(404, "Car doesn't exist")

        cars = model_to_dict(car)

        return get_success(200, cars, self.model.__name__)

    def post(self, request, *args, **kwargs):
        # data = request.body.decode('utf-8')
        # data_dict = json.loads(data)
        data_dict = request.POST
        form = self.modelForm(data_dict)
        if form.is_valid() :
            if int(kwargs['car_id']) in self.model.objects.values_list('pk', flat = True) :
                return self.update(kwargs['car_id'], data_dict)
            else:
                car = form.save()
                return get_success(201, model_to_dict(car), 'car')
        else :
            return _failure(400, form.errors)

    def update(self, car_id, data_dict):
        car = self.model.objects.get(pk = car_id)
        form = self.modelForm(data_dict, instance = car)
        car = form.save()
        return  get_success(202, model_to_dict(car), 'car')

class UserView(View):
    model = user
    submodel = car
    modelForm = UserForm

    def get(self, request, *args, **kwargs):
        try :
            user = self.model.objects.get(pk = kwargs['user_id'])
        except ObjectDoesNotExist:
            return _failure(404, "User doesn't exist")
        user_want = model_to_dict(user)
        fav = []
        if 'favourite' in [f.name for f in self.model._meta.get_fields()]:
            for car in user_want['favourite'] :
                fav.append(model_to_dict(car))
            user_want['favourite'] = fav

        car_sell = []
        if "car_sell" in [f.name for f in self.model._meta.get_fields()]:
            for car in user_want['car_sell'] :
                car_sell.append(model_to_dict(car))
            user_want['car_sell'] = car_sell

        return get_success(200, user_want, self.model.__name__)

    def post(self, request, *args, **kwargs):
        data = request.body.decode('utf-8')
        data_dict = json.loads(data)
        # data_dict = request.POST
        car_sell = set()
        if 'car_sell' in data_dict.keys():
            for i in data_dict['car_sell']:
                try :
                    obj = self.submodel.objects.get(pk=i)
                except ObjectDoesNotExist:
                    return _failure(404, 'requested car_sell list not valid (no such car in db)')
                car_sell.add(obj)
            data_dict["car_sell"] = car_sell

        fav = set()
        if 'favourite' in data_dict.keys():
            for i in data_dict['favourite']:
                try :
                    obj = self.submodel.objects.get(pk=i)
                except ObjectDoesNotExist:
                    return _failure(404, 'requested favourite list not valid (no such car in db)')
                fav.add(obj)
            data_dict['favourite'] = fav

        if int(kwargs['user_id']) in self.model.objects.values_list('pk', flat = True) :
            return self.update(kwargs['user_id'], data_dict)

        form = self.modelForm(data_dict)
        if form.is_valid():
            form.save()
            return _success(201, 'Create Success')
        else:
            return _failure(400, form.errors)

    def update(self, user_id, data_dict):
        user = self.model.objects.get(pk = user_id)
        form = self.modelForm(data_dict, instance = user)

        if form.is_valid():
            form.save()
            return _success(202, 'Update Success')
        else :
            return _failure(400, 'form invalid, bad post request.')

class DeleteCarView(DeleteView):
    model = car
    owner = user

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

            if 'favourite' in [f.name for f in self.model._meta.get_fields()]:
                if car in user.favourite.all():
                    user.favourite.remove(car)

class DeleteUserView(DeleteView):
    model = user
    submodel = car

    def delete(self, request, *args, **kwargs) :
        try :
            user = self.model.objects.get(pk = kwargs['user_id'])
        except ObjectDoesNotExist:
            return _failure(404, "User doesn't exist")
        if 'car_sell' in [f.name for f in self.model._meta.get_fields()] :
            for car in user.car_sell.all():
                self.Userdelete(car)
                car.delete()
        user.delete()
        return _success(202, 'Delete Success')

    def Userdelete(self, car) :
        for user in car.like.all():
            user.favourite.remove(car)

def signup(request):
    data_dict = request.POST
    form = UserForm(data_dict)
    if form.is_valid():
        user = form.save()
        user = model_to_dict(user)
        user.pop('car_sell', None)
        user.pop('favourite', None)
        user.pop('password', None)

        return get_success(201, user, 'user')
    else:
        return _failure(400, form.errors)
