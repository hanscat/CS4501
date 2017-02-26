import urllib.request, json
from django.http import JsonResponse, HttpResponse

# Create your views here.
modelsAPI = 'http://models-api:8000/api/v1/detail/'


def invalidURL(request):
    err = {}
    err['message'] = "Welcome to API page. Oops, you might just entered an invalid API request!"
    err['status'] = False
    return JsonResponse(err)


def demoCars(request, lb, ub):
    if request.method == 'GET':
        if (lb > ub):
            raise IndexError
        showingCars = {}
        for i in range(int(lb), int(ub) + 1):
            urlForParticularCar = modelsAPI + "car/"
            requester = urllib.request.Request(urlForParticularCar + str(i))
            response = urllib.request.urlopen(requester).read().decode('utf-8')
            car = json.loads(response)
            showingCars['car' + str(i)] = car
        return JsonResponse(showingCars)


def individualCarData(request, car_id):
    cars = "You are not using GET method!"
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "car/"
        requester = urllib.request.Request(urlForParticularCar + car_id)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        cars = json.loads(response)
    return JsonResponse(cars)


def showCertainColorCar(request, color):
    cars = "You are not using GET method!"
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "car/?car_color=" + color
        requester = urllib.request.Request(urlForParticularCar)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        cars = json.loads(response)
    return JsonResponse(cars)

def showCertainMakeCar(request, make):
    cars = "You are not using GET method!"
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "car/?car_make=" + make
        requester = urllib.request.Request(urlForParticularCar)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        cars = json.loads(response)
    return JsonResponse(cars)

# ==================>
def demoUsers(request, lb, ub):
    if request.method == 'GET':
        if (lb > ub):
            raise IndexError
        showingUsers = {}
        for i in range(int(lb), int(ub) + 1):
            urlForParticularUser = modelsAPI + "user/"
            requester = urllib.request.Request(urlForParticularUser + str(i))
            response = urllib.request.urlopen(requester).read().decode('utf-8')
            user = json.loads(response)
            showingUsers['user' + str(i)] = user
        return JsonResponse(showingUsers)


def individualUserData(request, user_id):
    user = "You are not using GET method!"
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "user/"
        requester = urllib.request.Request(urlForParticularCar + user_id)
        response = urllib.request.urlopen(requester).read().decode('utf-8')
        user = json.loads(response)
    return JsonResponse(user)


def showBuyers(request):
    # TO-DO
    return ""


def showSellers(request):
    # TO-DO
    return ""


def createUser(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        passwd = request.POST['password']
        # email = request.POST['email']

        data = {'user_name': username,
                'first_name': first_name,
                'last_name': last_name,
                'password': passwd, }

        url = modelsAPI + 'user/create/'
        data = urllib.parse.urlencode(data)
        data = data.encode('utf-8')  # data should be bytes
        req = urllib.request.Request(url, data)
        response = urllib.request.urlopen(req)
        ret = response.read().decode('utf-8')
        ret = json.loads(ret)
        retJSON = {}
        if (ret['status'] == True):
            retJSON['status'] = True
            retJSON['message'] = "User created"
        else:
            retJSON['status'] = False
            retJSON['message'] = "User failed to be created"
        return JsonResponse(retJSON)
