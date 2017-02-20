from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.views.generic import View, UpdateView, DeleteView
from django.db.models import Model
from django.forms import ModelForm

import json

def bad_request(request):
    return _failure(400, "Url not valid")

def internal_error(request):
    return _failure(500, "BOOM! I don't know what it going on now!")

def _failure(code, message):
    failure = {"Status Code" : code, "message" : message}
    return JsonResponse(failure)
