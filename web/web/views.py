from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import urllib.request, json
from django.core.urlresolvers import reverse
from .forms import UserInfo

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

def login_required(f):
    def wrap(request, *args, **kwargs):
        valid = check_status(request)
        if not valid:
            return HttpResponseRedirect(reverse('login')+ '?next=' + request.path)
        else:
            return f(request, *args, **kwargs)
    return wrap

@login_required
def user_detail(request, user_id):
    template = loader.get_template('home.html')
    url = expApi + "user/" + str(user_id)
    user = get_request(url)
    if user["status_code"] == 200 :
        user = [user["users"]]
        return render(request, 'userdetail.html', {'users': user})
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
                next = request.GET.get('next') or reverse('user_detail_page', kwargs={'user_id':user_id})
                response = HttpResponseRedirect(next)
                response.set_cookie('auth', auth)
                return response
            else:
                data = {}
                data['message'] = response["message"]
                data['userform'] = UserInfo()
                return render(request, 'login.html', data)
        return bad_request(request)
    else :
        return bad_request(request)

def logout(request):
    url = expApi + "logout/"
    #need to pass authenticator
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    ret = json.loads(response)
    if ret["status_code"] == 202 :# ==  True: --- If it returns Json, we want to pass and display message regardless
        message = [ret["message"]]
        return render(request, 'logout.html', {'message': message})
    else :
        return bad_request(request)

def signup(request):
    if request.method == "POST":
        signupdict = {}
        signupdict['user_name'] = request.POST['username']
        signupdict['password'] = request.POST['password']
        signupdict['retypepassword'] = request.POST['retypepassword']

        #if loginform.is_valid():
        if signupdict['password'] == signupdict['retypepassword']:
            url = expApi + "signup/"
            signup_data = json.dumps(signupdict).encode('utf8')
            requester = urllib.request.Request(url, data=signup_data, method='POST', headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(requester).read().decode('utf-8')
            ret = json.loads(response)
            if ret["status"]:# ==  True: --- If it returns Json, we want to pass and display message regardless
                message = [ret["message"]]
                return render(request, 'confirmsignup.html', {'message': message})
        return render(request, 'home.html') #invalid
    else:
        return render(request, 'signup.html')

def bad_request(request):
    template = loader.get_template('404.html')
    return HttpResponse(template.render(request))

def internal_error(request):
    template = loader.get_template('500.html')
    return HttpResponse(template.render(request))
