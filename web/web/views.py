from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import urllib.request, json
from .forms import UserInfo


expApi = 'http://exp-api:8000/api/v1/'
def index(request):
    template = loader.get_template('home.html')
    urlForCar = expApi + "democars/1to8"
    requester = urllib.request.Request(urlForCar)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    cars = json.loads(response)
    urlForUser= expApi + "user/1"
    requester = urllib.request.Request(urlForUser)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    user = json.loads(response)
    if cars["status_code"] == 200 :
        cars = cars["cars"]
        if user["status_code"] == 200:
            user = user["users"]
            user = [user]
        return render(request, 'home.html', {'cars': cars, 'users': user})
    else :
        return bad_request(request)

def login(request):
    if request.method == "POST":
        loginform = UserInfo(request.POST)
        logindict = {}
        logindict['username'] = request.POST['username']
        logindict['password'] = request.POST['password']

        if loginform.is_valid():
            url = expApi + "login/"
            login_data = json.dumps(logindict).encode('utf8')
            requester = urllib.request.Request(url, data=login_data, method='POST', headers={'Content-Type': 'application/json'})
            response = urllib.request.urlopen(requester).read().decode('utf-8')
            authvalue = json.loads(response)
            if authvalue["status"] ==  True:
                auth = [authvalue["auth"]]
                return render(request, 'home.html', {'auth': auth})
        return render(request, 'home.html') #invalid
    else:
        userform = UserInfo()
        return render(request, 'login.html', {'userform': userform})

def user_detail(request, user_id):
    template = loader.get_template('home.html')
    url = expApi + "user/" + str(user_id)
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    user = json.loads(response)
    if user["status_code"] == 200 :
        user = [user["users"]]
        return render(request, 'userdetail.html', {'users': user})
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

def logout(request):
    url = expApi + "logout/"
    #need to pass authenticator
    requester = urllib.request.Request(url)
    response = urllib.request.urlopen(requester).read().decode('utf-8')
    ret = json.loads(response)
    if ret["status"]:# ==  True: --- If it returns Json, we want to pass and display message regardless
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
