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
            return get_success(200, car, "cars")
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
            
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            data['model'] = 'user'
            producer.send('new-listings-topic', json.dumps(data).encode('utf-8'))

            # # add the listing to es
            es_add_user_listing(request, data["username"])

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
            data['model'] = 'car'
            producer.send('new-listings-topic', json.dumps(data).encode('utf-8'))
            
            # # add the listing to es
            es_add_car_listing(request, 999) #fake id
            
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
    search_string = post['search_query']
    search_index_specifier = post['query_specifier']
    
    elasticsearch_index = search_index_specifier + '_index'
    es = Elasticsearch(['es'])
    
    try:
        search_result = es.search(index=elasticsearch_index, body={
            "query": {'query_string': {'query': search_string}},
            'size': 100,
        })
    except:
        return _failure(400, 'improper search query!')

    result = {'status_code': 200}
    result['time_taken'] = search_result['took'] / 1000
    result['size'] = search_result['hits']['total']

    result['size_model'] = {'user': 0, 'car': 0}
    result['hits'] = []
    for item in search_result['hits']['hits']:
        detail = {'model': item['_source']['model']}

        if item['_source']['model'] == 'car':
            attributes = ['car_make', 'car_color', 'car_model', 'car_body_type', 'price', 'year']
            for attr in attributes:
                if attr in item['_source']:
                    detail['label'] += ': ' + item['_source'][attr]

            url = 'http://models-api:8000/api/detail/car/999/' # fake id
            resp = _make_get_request(url)

            detail['label'] += ' (' + resp['car']['car_make']
            detail['label'] += ' ' + resp['car']['car_color'] + ')'
        else:
            attributes = ['username', 'first_name', 'last_name']
            detail['label'] = ''
            for attr in attributes:
                if attr in item['_source']:
                    detail['label'] += ': ' + item['_source'][attr]
            url = 'http://models-api:8000/api/detail/user/' + item['_source']['username']
            url = 'http://models-api:8000/api/detail/user/2'
            resp = _make_get_request(url)
            detail['label'] += ' (' + resp['car']['car_make']
            detail['label'] += ' ' + resp['car']['car_color'] + ')'

        if detail['model'] == 'user':
            result['size_model']['user'] += 1
            detail['href'] = '/user/detail/' + item['_id'] + '/'
        else:
            result['size_model']['car'] += 1
            detail['href'] = '/car/detail/' + item['_id'] + '/'

        result['hits'].append(detail)

    # returns the final constructed data set
    return get_success(200, result, "search results")


# Helper
def es_add_user_listing(request, username): #username acts as unique id
    es = Elasticsearch(['es'])
    user_new_listing = {'first_name': request.POST['first_name'], 'last_name': request.POST['last_name'], 
                        'username': username, 'model': 'user'}
    es.index(index='user_index', doc_type='listing', id=user_new_listing['username'], body=user_new_listing)
    es.indices.refresh(index="user_index")


def es_add_car_listing(request, id):
    es = Elasticsearch(['es'])
    car_new_listing = {'car_make': request.POST['car_make'], 'description': request.POST['description'], 
                       'id': id, 'model': 'car'}
    es.index(index='car_index', doc_type='listing', id=car_new_listing['id'], body=car_new_listing)
    es.indices.refresh(index='car_index')

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
