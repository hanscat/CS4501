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

def search(request):
    if request.method == "GET":
        s_Form = searchForm()
        return render(request, 'search.html', {'form' : s_Form})
    elif request.method == "POST":
        s_Form = searchForm(request.POST)
        if s_Form.is_valid():
            url = expApi + "search/"
            search_data = s_Form.cleaned_data
            response= post_request(url, search_data)
            # return HttpResponse(response['search results'])
            if response['status_code'] == 200:
                return render(request, 'search_result.html', response['search results'])
            else :
                return HttpResponse("shit")
        return render(request, 'search.html', {'form' : s_Form})

def car_detail(request, car_id):
    template = loader.get_template('home.html')
    url = expApi + "car/"
    data = {}
    data["car_id"] = car_id
    if 'id' in request.COOKIES:
        data['user_id'] = request.COOKIES.get('id')
    else :
        data['user_id'] = 0
    car = post_request(url, data)
    if car["status_code"] == 200 :
        car = car["car"]
        return render(request, 'cardetail.html', {'car': car})
    else :
        return bad_request(request)

def check_status(request):
    if 'auth' not in request.COOKIES:
        return False
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
        valid = check_status(request)
        if valid:
            return HttpResponseRedirect(reverse('logout'))
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
    if 'auth' in request.COOKIES:
        auth = request.COOKIES.get('auth')
        post_data = {'auth': auth}
        resp = post_request(url, post_data)
        if resp["status_code"] == 202 :# ==  True: --- If it returns Json, we want to pass and display message regardless
            response = HttpResponseRedirect(reverse("logout"))
            response.delete_cookie('auth')
            response.delete_cookie('id')
            return response
        else :
            message = "Logout Success"
            return render(request, 'logout.html', {'message': message})
    else:
        message = "Logout Success"
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
                userform = SignupForm()
                error_message = []
                for key in message.keys():
                    error_message.append(message[key][0])
                return render(request, 'signup.html', {'SignupForm': userform, 'message': error_message})
            else:
                return render(request, 'confirmsignup.html')
        else :
            data = {}
            data['SignupForm'] = signupForm
            error_message = []
            for key in signupForm._errors.keys():
                error_message.append(signupForm._errors[key][0])
            data['message'] = error_message
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
            url = expApi + "car/create/"
            data = listForm.cleaned_data
            ret = post_request(url, data)
            message = "Car create fail"
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
        else:
            data = {}
            data['listForm'] = listForm
            error_message = []
            for key in listForm._errors.keys():
                error_message.append(listForm._errors[key][0])
            data['message'] = error_message
            return render(request, 'createListing.html', data)

    else :
        return HttpResponse("Bad Request")

def bad_request(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render(request))

def internal_error(request):
    template = loader.get_template('500.html')
    return HttpResponse(template.render(request))
