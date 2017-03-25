from django.http import JsonResponse, HttpResponse,HttpResponseRedirect
import urllib.request
import urllib.parse
import json


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


def _make_post_request(url, post_data):
    data = urllib.parse.urlencode(post_data).encode('utf-8')
    requester = urllib.request.Request(url, data=data, method='POST')
    response_json = urllib.request.urlopen(requester).read().decode('utf-8')
    response = json.loads(response_json)
    return response

'''Not yet tested'''
def createUser(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')
    else:
        data = request.body.decode('utf-8')
        post = json.loads(data)
        data = {}
        try:
            data["username"] = post["username"]
            data["password"] = post["password"]
            data["last_name"]= post["last_name"]
            data["first_name"] = post["first_name"]
        except KeyError:
            return _failure(400, 'missing parameters')

        url = modelsAPI + 'detail/user/999'
        user = _make_post_request(url, data)
        if user["status_code"] == 200 :
            user = user["user"]
            return get_success(200, user, "users")
        else :
            return model_failure(user)

"""Not yet tested"""
def check_loggedIn(request):
    # if ('auth' not in request.META):
    #     return False
    data = request.body.decode('utf-8')
    post = json.loads(data)
    data = {}
    try:
        data["auth"] = post["auth"]
    except KeyError:
        return False

    url = modelsAPI + 'auth/check_status'

    response = urllib.request.Request(url, data)
    status = json.loads(response)
    if status["status_code"] == 200:
        return True
    else:
        return model_failure(status)

'''Not yet tested'''
def login(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')
    else:
        data = request.body.decode('utf-8')
        post = json.loads(data)
        data = {}
        try:
            data["username"] = post["username"]
            data["password"] = post["password"]
        except KeyError:
            return _failure(400, 'missing parameters')

        url = modelsAPI + 'auth/login/'

        response = _make_post_request(url, data)
        if response["status_code"] == 200:
            return get_success(200, response, "login successfully")
        else:
            return model_failure(response)

'''Not yet tested'''
def logout(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post_data = request.body.decode('utf-8')
    post = json.loads(post_data)
    data={}
    try:
        data["auth"] = post["auth"]
    except KeyError:
        return _failure(400, 'missing parameters')

    url = modelsAPI + 'auth/logout/'

    response = _make_post_request(url, data)
    if response["status_code"] == 200:
        return get_success(200, response, "logout successfully")
    else:
        return model_failure(response)

    # else:
    #     data = request.body.decode('utf-8')
    #     post = json.loads(data)
    #     data = {}
    #     # return _success(200, 'authenticator', post)
    #     try:
    #         data['auth'] = post['auth']
    #     except KeyError:
    #         return _failure(400, 'missing parameters')
    #
    #     url = modelsAPI + 'auth/logout/'
    #     result = _make_post_request(url, data)
    #     if result["status_code"] == 200:
    #         return get_success(200, result, "auth")
    #     else:
    #         return model_failure(result)
def login_required(f):
    def wrap(request, *args, **kwargs):

        # try authenticating the user
        user = check_loggedIn(request)

        # authentication failed
        if not user:
            # redirect the user to the login page
            #return HttpResponseRedirect(reverse('login')+'?next='+current_url)
            """needs to be modified!"""
            return HttpResponseRedirect("https://www.google.com")
        else:
            return f(request, *args, **kwargs)
    return wrap


"""using decorator to write the create listing method"""
#@login_required
def createListing(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')
    else:
        data = request.body.decode('utf-8')
        post = json.loads(data)
        data = {}
        try:
            for key in ("car_year", "car_make", "car_model", "car_color",
                        "car_body_type", "car_new", "price"):
                data[key] = post[key]
            if post["description"]:
                data["description"] = post["description"]
        except KeyError:
            return _failure(400, 'missing parameters')

        url = modelsAPI + 'detail/car/9999'

        car = _make_post_request(url, data)
        if car["status_code"] == 200 :
            car = car["user"]
            return get_success(200, car, "cars")
        else :
            return model_failure(car)