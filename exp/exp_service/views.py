from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from kafka import KafkaProducer
from elasticsearch import Elasticsearch
import urllib.request
import urllib.parse
import json
import requests

# Create your views here.
modelsAPI = 'http://models-api:8000/api/v1/'


def _success(code, message):
    correct = {"status_code": code, "message": message}
    return JsonResponse(correct)


def _failure(code, message):
    failure = {"status_code": code, "message": message}
    return JsonResponse(failure)


def model_failure(modelResponse):
    return _failure(modelResponse["status_code"], modelResponse["message"])


def get_success(code, data_dict, model_name):
    correct = {"status_code": code, model_name: data_dict}
    return JsonResponse(correct)


def invalidURL(request):
    return _failure(404, "url not valid")


def _make_post_request(url, post_data):
    data = urllib.parse.urlencode(post_data).encode('utf-8')
    requester = urllib.request.Request(url, data=data, method='POST')
    response_json = urllib.request.urlopen(requester)
    response_json = response_json.read().decode('utf-8')
    response = json.loads(response_json)
    return response


def _make_get_request(url):
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    obj = json.loads(response)
    return obj


def _special_post_request(url, post_data):
    response = requests.post(url, data=json.dumps(post_data))
    return response


def home(request):
    if request.method == 'GET':
        ret = {}
        showingCars = []
        for i in range(1, 8):
            urlForParticularCar = modelsAPI + "detail/car/"
            car = _make_get_request(urlForParticularCar + str(i))
            if car["status_code"] == 200:
                car = car["car"]
                showingCars.append(car)
        ret["cars"] = showingCars

        showingUsers = []
        for i in range(1, 2):
            urlForParticularUser = modelsAPI + "detail/user/"
            user = _make_get_request(urlForParticularUser + str(i))
            if user["status_code"] == 200:
                user = user["user"]
            showingUsers.append(user)
        ret["users"] = showingUsers

        return get_success(200, ret, "ret")
    else:
        return _failure(405, "Methods not supported")


def car_detail(request, car_id):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/car/"
        car = _make_get_request(urlForParticularCar + car_id)
        if car["status_code"] == 200:
            car = car["car"]
            return get_success(200, car, "car")
        else:
            return model_failure(car)
    else:
        return _failure(405, "Methods not supported")


# def showCertainColorCar(request, color):
#     if request.method == 'GET':
#         urlForParticularCar = modelsAPI + "detail/car/?car_color=" + color
#         requester = urllib.request.Request(urlForParticularCar)
#         response = urllib.request.urlopen(requester).read().decode('utf-8')
#         cars = json.loads(response)
#         if cars["status_code"] == 200:
#             car = cars["car"]
#             return get_success(200, cars, "cars")
#         else :
#             return model_failure(cars)
#     else :
#         return _failure(405, "Methods not supported")
#
# def showCertainMakeCar(request, make):
#     if request.method == 'GET':
#         urlForParticularCar = modelsAPI + "detail/car/?car_make=" + make
#         requester = urllib.request.Request(urlForParticularCar)
#         response = urllib.request.urlopen(requester).read().decode('utf-8')
#         cars = json.loads(response)
#         if cars["status_code"] == 200:
#             car = cars["car"]
#             return get_success(200, cars, "cars")
#         else :
#             return model_failure(cars)
#     else :
#         return _failure(405, "Methods not supported")

def user_detail(request, user_id):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/user/"
        user = _make_get_request(urlForParticularCar + user_id)
        if user["status_code"] == 200:
            user = user["user"]
            return get_success(200, user, "users")
        else:
            return model_failure(user)
    else:
        return _failure(405, "Methods not supported")


def concise_user_detail(request, user_id):
    if request.method == 'GET':
        urlForParticularCar = modelsAPI + "detail/user/"
        user = _make_get_request(urlForParticularCar + user_id)
        if user["status_code"] == 200:
            user = user["user"]
            index_list = []
            for car in user['car_sell']:
                index_list.append(car['id'])
            user['car_sell'] = index_list
            index_list = []
            for car in user['favourite']:
                index_list.append(car['id'])
            user['favourite'] = index_list
            return get_success(200, user, "users")
        else:
            return model_failure(user)
    else:
        return _failure(405, "Methods not supported")


def update_user(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')
    else:
        data = request.body.decode('utf-8')
        post = json.loads(data)
        data = {}
        try:
            for key in ("first_name", "id", "last_name", "password", "username", "car_sell", "favourite"):
                data[key] = post[key]
        except KeyError:
            return _failure(400, 'missing parameters')
        url = modelsAPI + 'detail/user/' + str(data["id"])
        # return HttpResponse(url)
        data.pop("id", None)
        user = _special_post_request(url, data)
        return _success(201, 'Create Success')


def create_user(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')
    else:
        post = request.POST
        data = {}
        try:
            data["username"] = post["username"]
            data["password"] = post["password"]
            data["last_name"] = post["last_name"]
            data["first_name"] = post["first_name"]
        except KeyError:
            return _failure(400, 'missing parameters')
        url = modelsAPI + 'signup/'
        user = _make_post_request(url, data)
        if user["status_code"] == 201:
            user = user['user']
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            new_user = {}
            new_user['model'] = 'api.user'
            new_user['fields'] = dict(user)
            new_user['pk'] = user['id']
            producer.send('new-listings-topic', json.dumps(new_user).encode('utf-8'))

            # return the json
            return get_success(201, user, "users")
        else:
            return model_failure(user)


def create_car(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')
    else:
        post = request.POST
        data = {}
        try:
            for key in ("car_year", "car_make", "car_model", "car_color",
                        "car_body_type", "car_new", "price", "description"):
                data[key] = post[key]

        except KeyError:
            return _failure(400, 'missing parameters')
        url = modelsAPI + 'detail/car/9999'
        car = _make_post_request(url, data)
        if car["status_code"] == 201:
            # send data to Kafka
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            new_car = {}
            new_car['model'] = 'api.car'
            new_car['pk'] = car['car']['id']
            new_car['fields'] = dict(car['car'])
            new_car['fields']['car_new'] = int(new_car['fields']['car_new'])
            producer.send('new-listings-topic', json.dumps(new_car).encode('utf-8'))

            # return the json
            car = car["car"]
            return get_success(201, car, "car")
        else:
            return _failure(car['status_code'], "Model layer error")


def check_loggedIn(request):
    post = request.POST
    data = {}
    try:
        data["auth"] = post["auth"]
    except KeyError:
        return False

    url = modelsAPI + 'auth/check_status/'
    response = _make_post_request(url, data)
    if response["status_code"] == 200:
        return _success(200, "validated")
    else:
        return model_failure(response)


def login(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')
    else:
        # data = request.body.decode('utf-8')
        # post = json.loads(data)
        post = request.POST
        data = {}
        try:
            data["username"] = post["username"]
            data["password"] = post["password"]
        except KeyError:
            return _failure(400, 'missing parameters')
        url = modelsAPI + 'auth/login/'
        response = _make_post_request(url, data)
        if response["status_code"] == 200:
            return get_success(200, response["authenticator"], "authenticator")
        else:
            return model_failure(response)


def logout(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post = request.POST
    data = {}
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


#########################
def search(request):
    if request.method != 'POST':
        return _failure(400, 'incorrect request type')

    post = request.POST
    search_string = post['query']
    search_index_specifier = post['query_specifier']

    elasticsearch_index = search_index_specifier + '_index'
    es = Elasticsearch(['es'])
    search_result = es.search(index=elasticsearch_index, body={
        "query": {'query_string': {'query': search_string}},
        'size': 100,
    })

    result = {}
    result['time_taken'] = search_result['took'] / 1000
    result['size'] = search_result['hits']['total']

    result['size_model'] = {'user': 0, 'car': 0}
    result['hits'] = {}
    car_list = []
    user_list = []
    for item in search_result['hits']['hits']:
        car_detail = {}
        user_detail = {}
        if item['_source']['model'] == 'api.car':
            attributes = ['car_make', 'car_color', 'car_model', 'car_body_type', 'price', 'year']
            for attr in attributes:
                if attr in item['_source']['fields']:
                    car_detail[attr] = item['_source']['fields'][attr]
            car_detail['id'] = item['_source']['fields']['id']
            result['size_model']['car'] += 1
            car_list.append(car_detail)
        else:
            attributes = ['username', 'first_name', 'last_name']
            for attr in attributes:
                if attr in item['_source']['fields']:
                    user_detail[attr] = item['_source']['fields'][attr]

            user_detail['id'] = item['_source']['fields']['id']
            result['size_model']['user'] += 1
            user_list.append(user_detail)

    result['hits']['car_list'] = car_list
    result['hits']['user_list'] = user_list

    # returns the final constructed data set
    return get_success(200, result, "search results")

# """TO-DO"""
# def showBuyers(request):
#     if request.method == 'GET':
#         urlForSearchingUser = modelsAPI + "detail/user/"
#         requester = urllib.request.Request(urlForSearchingUser)
#         response = urllib.request.urlopen(requester).read().decode('utf-8')
#         user = json.loads(response)
#         if user["status_code"] == 200 :
#             user = user["user"]
#             return get_success(200, user, "users")
#         else :
#             return model_failure(user)
#     else :
#         return _failure(405, "Methods not supported")
#
# def showSellers(request):
#     # TO-DO
#     return ""


# def demoUsers(request, lb, ub):
#     if request.method == 'GET':
#         if (lb > ub):
#             return _failure(404, "Index error")
#         showingUsers = []
#         for i in range(int(lb), int(ub) + 1):
#             urlForParticularUser = modelsAPI + "detail/user/"
#             requester = urllib.request.Request(urlForParticularUser + str(i))
#             response = urllib.request.urlopen(requester).read().decode('utf-8')
#             user = json.loads(response)
#             if user["status_code"] == 200:
#                 user = user["user"]
#             showingUsers.append(user)
#         return get_success(200, showingUsers, "users")
#     else :
#         return _failure(405, "Methods not supported")
#
# def demoCars(request, lb, ub):
#     if request.method == 'GET':
#         if (lb > ub):
#             return _failure(404, "Index error")
#         showingCars = []
#         for i in range(int(lb), int(ub) + 1):
#             urlForParticularCar = modelsAPI + "detail/car/"
#             requester = urllib.request.Request(urlForParticularCar + str(i))
#             response = urllib.request.urlopen(requester).read().decode('utf-8')
#             car = json.loads(response)
#             if car["status_code"] == 200:
#                 car = car["car"]
#                 showingCars.append(car)
#         return get_success(200, showingCars, "cars")
#     else :
#         return _failure(405, "Methods not supported")
