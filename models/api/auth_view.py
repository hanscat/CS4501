from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.views.generic import View, UpdateView, DeleteView
from .models import *
from .forms import *
from django.db.models import Model
from django.forms import ModelForm
from django.contrib.auth import hashers
from django.utils import timezone
import os
import hmac
import json
import datetime
import models.settings

def _success(code, model_name, data_dict):
    correct = {"status_code" : code, model_name : data_dict }
    return JsonResponse(correct)

def message_success(code, message):
    correct = {"status_code" : code, "message" : message}
    return JsonResponse(correct)

def _failure(code, message):
    failure = {"status_code" : code, "message" : message}
    return JsonResponse(failure)

def login(request):
    if request.method != 'POST':
        return _failure(500, 'request not supported')
    post = request.POST
    try :
        username = post['username']
        password = post['password']
    except KeyError:
        return _failure(400, 'missing parameters')
    try :
        login_user = user.objects.get(user_name = username)
        userid = login_user.pk
    except ObjectDoesNotExist:
        return _failure(404, 'user not found')

    if not hashers.check_password(password, login_user.password):
    # if password != login_user.password:
        return _failure(403, 'incorrect password')

    token = hmac.new(
    key = models.settings.SECRET_KEY.encode('utf-8'),
    msg = os.urandom(32),
    digestmod = 'sha256'
    ).hexdigest()
    auth = Authenticator(userid=userid,auth=token)
    auth.save()
    data = model_to_dict(auth)
    return _success(200, 'authenticator', data)

def check_status(request):
    if request.method != 'POST':
        return _failure(500, 'request not supported')
    post = request.POST
    try :
        token = post['auth']
    except KeyError:
        return _failure(400, 'missing parameters')
    try:
        auth = Authenticator.objects.get(auth=token)
    except ObjectDoesNotExist:
        return _failure(403, 'authenticator not found')
    time = timezone.now() - auth.date_created
    if time.total_seconds() > 100:
        auth.delete()
        return message_success(202, "timeout, automatically logout")
    else :
        return message_success(200, 'valid auth')


def logout(request):
    if request.method != 'POST':
        return _failure(500, 'request not supported')
    post = request.POST
    try :
        token = post['auth']
    except KeyError:
        return _failure(400, 'missing parameters')
    try:
        auth = Authenticator.objects.get(auth=token)
    except ObjectDoesNotExist:
        return _failure(403, 'authenticator not found')
    auth.delete()
    return message_success(202, "logout success")

# only for testing not deployed onto urls
def deleteAllAuth(request):
    authenticator.objects.all().delete()
    return message_success(200, "You made a bad choicd")
