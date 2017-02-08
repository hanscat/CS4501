from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Welcome to API page.")
