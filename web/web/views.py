from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import urllib.request, json
from django.core.urlresolvers import reverse
from .forms import *
import requests

def get_request(url):
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def post_request(url, post_data):
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request(url, data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp

def special_post_request(url, post_data):
    response = requests.post(url, data=json.dumps(post_data)).json()
    return response

expApi = 'http://exp-api:8000/api/v1/'
def index(request):
    url = expApi + "home"
    ret = get_request(url)
    if ret["status_code"] == 200 :
        cars = ret['ret']['cars']
        user = ret['ret']['users']
        return render(request, 'home.html', {'cars': cars, 'users': user})
    else :
        return bad_request(request)

def car_detail(request, car_id):
    template = loader.get_template('home.html')
    url = expApi + "car/" + str(car_id)
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    car = json.loads(response)
    if car["status_code"] == 200 :
        car = [car["cars"]]
        return render(request, 'cardetail.html', {'cars': car})
    else :
        return bad_request(request)

def check_status(request):
    auth = request.COOKIES.get('auth')
    post_data = {'auth': auth}
    url = 'http://exp-api:8000/api/v1/auth/check_status/'
    resp = post_request(url, post_data)
    return resp['status_code'] == 200

def load_user(request):
    id = request.COOKIES.get('id')
    url = 'http://exp-api:8000/api/v1/user/' + str(id)
    user = get_request(url)
    return user

def load_concise_user(request):
    id = request.COOKIES.get('id')
    url = 'http://exp-api:8000/api/v1/user/concise/' + str(id)
    user = get_request(url)
    return user


def login_required(f):
    def wrap(request, *args, **kwargs):
        valid = check_status(request)
        if not valid:
            return HttpResponseRedirect(reverse('login')+ '?next=' + request.path)
        else:
            return f(request, *args, **kwargs)
    return wrap

@login_required
def user_detail(request):
    template = loader.get_template('home.html')
    user = load_user(request)
    if user["status_code"] == 200 :
        user = user["users"]
        return render(request, 'userdetail.html', {'user': user})
    else :
        return bad_request(request)

def login(request):
    # check current_status first
    if request.method == "GET":
        userform = UserInfo()
        data = {}
        data['userform'] = userform
        return render(request, 'login.html', data)
    elif request.method == "POST":
        loginform = UserInfo(request.POST)
        if loginform.is_valid():
            url = expApi + "auth/login/"
            login_data = loginform.cleaned_data
            response= post_request(url, login_data)
            if response["status_code"]==200:
                authenticator = response['authenticator']
                auth = authenticator['auth']
                user_id = authenticator['userid']
                next = request.GET.get('next') or reverse('user_detail_page')
                response = HttpResponseRedirect(next)
                response.set_cookie('auth', auth)
                response.set_cookie('id', user_id)
                return response
            else:
                data = {}
                data['message'] = response["message"]
                data['userform'] = UserInfo()
                return render(request, 'login.html', data)
        data = {}
        data['userform'] = UserInfo()
        return render(request, 'login.html', data)
    else:
        return bad_request(request)

def logout(request):
    url = expApi + "auth/logout/"
    #need to pass authenticator
    auth = request.COOKIES.get('auth')
    post_data = {'auth': auth}
    resp = post_request(url, post_data)
    if resp["status_code"] == 202 :# ==  True: --- If it returns Json, we want to pass and display message regardless
        message = "Logout Success"
        return render(request, 'logout.html', {'message': message})
    else :
        message = "Already Logout"
        return render(request, 'logout.html', {'message': message})

def signup(request):
    if request.method == "GET":
        userform = SignupForm()
        data = {}
        data['SignupForm'] = userform
        return render(request, 'signup.html', data)
    elif request.method == "POST":
        signupForm = SignupForm(request.POST)
        if signupForm.is_valid():
            url = expApi + "user/signup/"
            data = signupForm.cleaned_data
            data.pop('password_repeat', None)
            ret= post_request(url, data)
            if ret["status_code"] != 201:
                message = ret["message"]
                return render(request, 'signup.html', {'message': message})
            else:
                return HttpResponseRedirect(reverse('login'))
        else :
            data = {}
            data['SignupForm'] = signupForm
            data['message'] = "BAD INPUT"
            return render(request, 'signup.html', data)
    else :
        return HttpResponse("Bad Request")

@login_required
def createListing(request):
    if request.method == "GET":
        listForm = listingForm()
        data = {}
        data['listForm'] = listForm
        return render(request, 'createListing.html', data)
    elif request.method == "POST":
        listForm = listingForm(request.POST)
        if listForm.is_valid():
            url = expApi + "createCar/"
            data = listForm.cleaned_data
            ret = post_request(url, data)
            if ret["status_code"] != 201:
                return render(request, 'createListing.html', {'message': message})
            else :
                car_id = ret['car']['id']
                userid = request.COOKIES.get('id')
                user = load_concise_user(request)['users']
                user["car_sell"].append(car_id)
                url = expApi + 'user/update/'
                response = special_post_request(url, user)
                if response["status_code"] == 201:
                    return HttpResponseRedirect(reverse('user_detail_page'))
                else :
                    return HttpResponseRedirect(reverse('createListing'))
    else :
        return HttpResponse("Bad Request")

def bad_request(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render(request))

def internal_error(request):
    template = loader.get_template('500.html')
    return HttpResponse(template.render(request))
