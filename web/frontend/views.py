from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render(request))

def user_detail(request):
    template = loader.get_template('userdetail.html')
    return HttpResponse(template.render(request))

def car_detail(request):
    template = loader.get_template('cardetail.html')
    return HttpResponse(template.render(request))