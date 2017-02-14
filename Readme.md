##Web Application for CS 4501: P2P Used Car Sale

##Project 2 Timeline:

1. 2017-02-08:
    1. models container setup
    2. testing models setup
    3. views.py , urls.py updated


2. 2017-02-09:
    1. json post/get method setup, usage see below


3. 2017-02-13:
    1. json fixture
    2. docker-compose file
    3. url restructure
    4. curd all created and tested

##Model
* seller
  * first_name 'CharField'
  * last_name 'CharField'
  * username 'CharField' 'Unique'
  * password 'CharField'
  * car_sell 'ManyToManyField' list of car_to_sell types
  * id(pk) 'PrimaryKey' set by default Automatically increment when new seller inserted


* buyer
  * all fields in seller except car_sell
  * favourite 'ManyToManyField' list of car_to_buy types


* car_to_sell
  * car_color
  * car_brand
  * car_model
  * price
  * description
  * price_to_sell


* car_to_buy
  * all fields in seller except price_to_sell
  * price_to_offer


##Workable urls

    localhost:8001/api/v1/detail/seller/[0-9]+
    localhost:8001/api/v1/detail/buyer/[0-9]+
    localhost:8001/api/v1/detail/sell_car/[0-9]+
    localhost:8001/api/v1/detail/buy_car/[0-9]+
    localhost:8001/api/v1/delete/seller/[0-9]+
    localhost:8001/api/v1/delete/seller/[0-9]+
    localhost:8001/api/v1/delete/sell_car/[0-9]+
    localhost:8001/api/v1/delete/buy_car/[0-9]+

##API Documentation

1. GET /detail/<model>/<id>[0-9]+

    * Response: a JSON response containing the information of the model with id(pk) given.

    * Status
      * '200' if object found
      * '404' if object not found


2. POST /detail/<model>/<id>[0-9]+
    * Post: valid JSON table for corresponding model

    * Status:
      * '400': if form posted not valid
      * '404': if form posted valid but in 'ManyToManyField' contains invalid id in corresponding model(car)
      * '201' if <id> not found in db, automatically create new object by the given info **the new object will not have the pk(id) given in the url, system will automatically assign one id to it**
      * '202' if <id> found in db, update new object by the given info


3. POST /delete/<model>/<id>[0-9]+
    * Post: nothing required

    * Status:
      * '404': if object not found
      * '202': if object found and deleted






        <!-- "first_name": "new",

        "last_name": "user",

        "user_name": "newuser",

        "password": "12345678",

        "car_own": ""

    otherwise return "Bad Request"

    2. 8001/api/create/user/buyer


        "first_name": "new",

        "last_name": "user",

        "user_name": "newuser",

        "password": "12345678",

        "car_want": ""


    otherwise return "Bad Request" -->
