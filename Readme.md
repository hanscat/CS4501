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
  * first_name `CharField`
  * last_name `CharField`
  * username `CharField` `Unique`
  * password `CharField`
  * car_sell `ManyToManyField` list of car_to_sell types
  * id(pk) `PrimaryKey` set by default Automatically increment when new seller inserted


* buyer
  * all fields in seller except car_sell
  * favourite `ManyToManyField` list of car_to_buy types


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

##API

1. GET /detail/[model]/[id][0-9]+

    * Response: a JSON response containing the information of the model with `id` given

    * Status
      * `200` if object found
      * `404` if object not found


2. POST /detail/[model]/[id][0-9]+
    * Post: valid JSON table for corresponding model.

    * Status:
      * `400`: if form posted not valid.
      * `404`: if form posted is valid, but 'ManyToManyField' contains invalid id in corresponding model(car).
      * `201`: if `id` not found in db, automatically create new object by the given info. **Note: the new object will not have the `id` given in the url, system will automatically assign one id to it**.
      * `202`: if `id` found in db, update new object by the given info.


3. POST /delete/[model]/[id][0-9]+
    * Post: nothing required

    * Status:
      * `404`: if object not found
      * `202`: if object found and deleted

##Example Json Post Format

        //userModel(buyer & seller)

        {
        "first_name": "new",

        "last_name": "user",

        "user_name": "newuser",

        "password": "12345678",

        "car_sell": [1,2,3]   //for seller, optional

        "favourite": [1,2,3]  //for buyer, optional
        }

        //carModel(car_to_sell & car_to_buy)

        {
        "car_color": "black",

        "car_brand": "Benz",

        "car_model": "G63",

        "description": "This is a car."

        "price": "9999"

        "price_to_sell": "15000" //for car_to_sell

        "price_to_offer": "7000" //for car_to_buy
        }
