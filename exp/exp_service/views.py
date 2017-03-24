import urllib.request, json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json, requests
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect, csrf_exempt

# Create your views here.
modelsAPI = 'http://models-api:8000/api/v1/'


def _success(code, message):
    correct = {"status_code": code, "message": message}
    return JsonResponse(correct)


def _failure(code, message):
    failure = {"status_code": code, "message": message}
    return JsonResponse(failure)

def model_failure(modelResponse):
    return _failure(modelResponse["status_code"], modelResponse["message"] + ", triggered in model layer")


def get_success(code, data_dict, model_name):
    correct = {"status_code": code, model_name: data_dict}
    return JsonResponse(correct)


def invalidURL(request):
    return _failure(404, "url not valid")


def demoCars(request, lb, ub):
    if request.method == 'GET':
        if (lb > ub):
            return _failure(404, "Index error")
        showingCars = []
        for i in range(int(lb), int(ub) + 1):
            urlForParticularCar = modelsAPI + "detail/car/"
            requester = urllib.request.Request(urlForParticularCar + str(i))
            response = urllib.request.urlopen(requester).read().decode('utf-8')
            car = json.loads(response)
            if car["status_code"] == 200:
                car = car["car"]
                showingCars.append(car)
        return get_success(200, showingCars, "cars")
    else :
        return _failure(405, "Methods not supported")

def individualCarData(request, car_id):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/car/"
        requester = urllib.request.Request(urlForParticularCar + car_id)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        car = json.loads(response)
        if car["status_code"] == 200:
            car = car["car"]
            return get_success(200, car, "cars")
        else :
            return model_failure(car)
    else:
        return _failure(405, "Methods not supported")

def showCertainColorCar(request, color):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/car/?car_color=" + color
        requester = urllib.request.Request(urlForParticularCar)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        cars = json.loads(response)
        if cars["status_code"] == 200:
            car = cars["car"]
            return get_success(200, cars, "cars")
        else :
            return model_failure(cars)
    else :
        return _failure(405, "Methods not supported")

def showCertainMakeCar(request, make):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/car/?car_make=" + make
        requester = urllib.request.Request(urlForParticularCar)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        cars = json.loads(response)
        if cars["status_code"] == 200:
            car = cars["car"]
            return get_success(200, cars, "cars")
        else :
            return model_failure(cars)
    else :
        return _failure(405, "Methods not supported")

def demoUsers(request, lb, ub):
    if request.method == 'GET':
        if (lb > ub):
            return _failure(404, "Index error")
        showingUsers = []
        for i in range(int(lb), int(ub) + 1):
            urlForParticularUser = modelsAPI + "detail/user/"
            requester = urllib.request.Request(urlForParticularUser + str(i))
            response = urllib.request.urlopen(requester).read().decode('utf-8')
            user = json.loads(response)
            if user["status_code"] == 200:
                user = user["user"]
            showingUsers.append(user)
        return get_success(200, showingUsers, "users")
    else :
        return _failure(405, "Methods not supported")


def individualUserData(request, user_id):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/user/"
        requester = urllib.request.Request(urlForParticularCar + user_id)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        user = json.loads(response)
        if user["status_code"] == 200 :
            user = user["user"]
            return get_success(200, user, "users")
        else :
            return model_failure(user)
    else :
        return _failure(405, "Methods not supported")
"""TO-DO"""
def showBuyers(request):
    if request.method == 'GET':
        urlForSearchingUser = modelsAPI + "detail/user/"
        requester = urllib.request.Request(urlForSearchingUser)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        user = json.loads(response)
        if user["status_code"] == 200 :
            user = user["user"]
            return get_success(200, user, "users")
        else :
            return model_failure(user)
    else :
        return _failure(405, "Methods not supported")


def showSellers(request):
    # TO-DO
    return ""

'''Not yet tested'''
@csrf_exempt
@require_http_methods(["POST"])
def createUser(request):
    if request.method == 'POST':

        url = modelsAPI + 'create/user/'

        username = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        # email = request.POST['email']
        data = {'user_name': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': password, }

        data = urllib.parse.urlencode(data).encode('utf-8')  # data should be bytes
        requester = urllib.request.Request(url, data)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        user = json.loads(response)
        if user["status_code"] == 200 :
            user = user["user"]
            return get_success(200, user, "users")
        else :
            return model_failure(user)

"""Not yet tested"""
def user_logged_in(request):
    if ('Authenticator' not in request.META):
        return False
    auth = request.META.get('Authenticator')
    url = modelsAPI + 'auth/check_status'
    data = {'Authenticator': auth}
    response = urllib.request.Request(url, data)
    status = json.loads(response)
    if status["status_code"] == 200:
        return get_success(200, status, "Authenticator")
    else:
        return model_failure(status)

'''Not yet tested'''
@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    if request.method == 'POST':
        user_id = request.POST['username']
        password = request.POST['password']

        data = {'username': user_id,
                'password': password}

        url = modelsAPI + 'auth/login/'
        data = urllib.parse.urlencode(data).encode('utf-8')  # data should be bytes
        requester = urllib.request.Request(url, data)
        response = urllib.request.urlopen(requester)
        result = json.loads(response.read().decode('utf-8'))
        if result["status_code"] == 200:
            return get_success(200, result, "Authenticator")
        else:
            return model_failure(result)

'''Not yet tested'''
@csrf_exempt
@require_http_methods(["POST"])
def logout(request):
    if request.method == 'POST':
        auth = request.POST['Authenticator']
        data = {'Authenticator': auth}
        url = modelsAPI + 'auth/logout/'
        data = urllib.parse.urlencode(data).encode('utf-8')  # data should be bytes
        requester = urllib.request.Request(url, data)
        response = urllib.request.urlopen(requester)
        result = json.loads(response.read().decode('utf-8'))
        if result["status_code"] == 200:
            return get_success(200, result, "Authenticator")
        else:
            return model_failure(result)



"""using decorator to write the create listing method"""