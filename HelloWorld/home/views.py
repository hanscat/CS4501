from django.shortcuts import render, render_to_response

# Create your views here.

def homePage(request):
    lst = ["http://buyersguide.caranddriver.com/media/assets/submodel/7821.jpg",
           "http://buyersguide.caranddriver.com/media/assets/submodel/7651.jpg",
           "http://buyersguide.caranddriver.com/media/assets/submodel/4877.jpg"]
    return render_to_response("homePage.html", {'name': 'Kefan Zhang (kz6ef)', 'list': lst})