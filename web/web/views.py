from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render(request))

def user_detail(request):
    template = loader.get_template('userdetail.html')
    return HttpResponse(template.render(request))

def car_detail(request):
    template = loader.get_template('cardetail.html')
    return HttpResponse(template.render(request))

def bad_request(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render(request))

def internal_error(request):
    template = loader.get_template('500.html')
    return HttpResponse(template.render(request))
