##Web Application for CS 4501: P2P Used Car Sale

##Project 2 Timeline:

1. 2017-02-08:
    1. models container setup
    2. testing models setup
    3. views.py , urls.py updated

2. 2017-02-09:
    1. json post/get method setup, usage see below

2. To do:
    1. finalize models
    2. json fixture
    3. docker-compose file
    4. url restructure

##Workable urls
1. GET :
    1. 8001/api: return index page
    2. 8001/api/user/seller/[1-9]+: return json format seller(pk = id) if exists
    3. 8001/api/user/buyer/[1-9]+: return json format buyer(pk=id) if exists
    4. 8001/api/car/sell/[1-9]+: return json format car_to_sell(pk=id) if exists
    5. 8001/api/car/buy/[1-9]+: return json format car_to_sell(pk=id) if exists

2. POST :
    1. 8001/api/create/user/seller: accept format

    {
        "first_name": "new",

        "last_name": "user",

        "user_name": "newuser",

        "password": "12345678",

        "car_own": ""
    }

    otherwise return "Bad Request"

    2. 8001/api/create/user/buyer

    {

        "first_name": "new",

        "last_name": "user",

        "user_name": "newuser",

        "password": "12345678",

        "car_want": ""

    }

    otherwise return "Bad Request"
