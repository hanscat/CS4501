import urllib.request, json
from django.http import JsonResponse, HttpResponse

# Create your views here.
modelsAPI = 'http://models-api:8000/api/v1/detail/'


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
            urlForParticularCar = modelsAPI + "car/"
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
        urlForParticularCar = modelsAPI + "car/"
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
        urlForParticularCar = modelsAPI + "car/?car_color=" + color
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
        urlForParticularCar = modelsAPI + "car/?car_make=" + make
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
            urlForParticularUser = modelsAPI + "user/"
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
        urlForParticularCar = modelsAPI + "user/"
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
def showBuyers(request):
    # TO-DO
    return ""


def showSellers(request):
    # TO-DO
    return ""

# Not yet tested
# def createUser(request):
#     if request.method == 'POST':
#         username = request.POST['user_name']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         passwd = request.POST['password']
#         # email = request.POST['email']
#
#         data = {'user_name': username,
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'password': passwd, }
#
#         url = modelsAPI + 'user/create/'
#         data = urllib.parse.urlencode(data)
#         data = data.encode('utf-8')  # data should be bytes
#         req = urllib.request.Request(url, data)
#         response = urllib.request.urlopen(req)
#         ret = response.read().decode('utf-8')
#         ret = json.loads(ret)
#         retJSON = {}
#         if (ret['status'] == True):
#             retJSON['status'] = True
#             retJSON['message'] = "User created"
#         else:
#             retJSON['status'] = False
#             retJSON['message'] = "User failed to be created"
#         return get_success(200, retJSON, "users")
