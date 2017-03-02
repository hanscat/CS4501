##Web Application for CS 4501: college P2P Used Car Sale/Trade

##Project 3 Timeline:
1. 2017-02-17:
    1. User stories written

2. 2017-02-19:
    1. models, views, urls reset for further implementation, detail see sections below
    2. api's for experience tier created based on user stories and tested to function well

3. 2017-02-23:
    1. test for models
    2. minor update for trivial text

4. 2017-02-26:
    1. frontend page launched
    2. exp layer setup and api provided

5. 2017-02-28:
    1. frontend and exp connected
    2. index page, car detail page, user detail page, error page created and tested

6. 2017-03-01:
    1. sidebar for recommended user created
    2. header2 created
    3. project finalized

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

##URL
* localhost:8000: index page, contain several car information, and a user information
  * the brandname in the header links(in all pages) to the index page
  * the `viewDetail` lead to the corresponding car page
  * the link under `user` all lead to the same user page
* localhost:8000/cardetail/<id>: cardetail page, contain information of a car
* localhost:8000/userdetail/<id>: userdetail page, contain information of a user

**if given id the car/user not found turn to a 404 error page**

##Test
To run test please do the following:
  * set a docker container (using tp33/django as image) containing the whole `app` folder, run following assume you have a clean database directory `db` parallel to `app`
  ```bash
  $ docker run -it --name web -p 8000:8000 --link mysql:db -v ~/absolute/directory/to/app:/app tp33/django
  $ docker exec -it web bash
  ```
  * move into model layer
  ```bash
  $ cd models
  ```
  * run test using manage.py
  ```bash
  $ python manage.py test
  ```

  * you shall expect to see the following
  ```bash
  Creating test database for alias 'default'...
  ...........
    ----------------------------------------------------------------------
  Ran 11 tests in 1.828s

  OK
  ```

##Model
* user
  * first_name `CharField`
  * last_name `CharField`
  * user_name `CharField` `Unique`
  * password `CharField`
  * car_sell `ManyToManyField` `optional` list of car types
  * favourite `ManyToManyField` `optional` list of car types
  * id(pk) `PrimaryKey` set by default Automatically increment when new user inserted


* car_to_sell
  * car_color `CharField`
  * car_brand `CharField`
  * car_model `CharField`
  * price `IntegerField`
  * description `IntegerField`
  * id(pk) `PrimaryKey` set by default Automatically increment when new car inserted


##Workable urls

    localhost:8001/api/v1/detail/user/[0-9]+
    localhost:8001/api/v1/detail/user/?[fields]=[instance]&  
    localhost:8001/api/v1/detail/car/[0-9]+
    localhost:8001/api/v1/detail/car/?[fields]=[instance]&
    localhost:8001/api/v1/delete/user/[0-9]+
    localhost:8001/api/v1/delete/car/[0-9]+

##API

* GET detail/user/?[fields]=[instance]&

    * Response: a JSON response containing a list of objects follow the constraints sent

    * Status:
      * `200`: if objects found
      * `404`: if objects not fount
      * `404`: if fields specified are not valid in the corresponding model

* GET /detail/[model]/[id][0-9]+

    * Response: a JSON response containing the information of the model with `id` given

    * Status
      * `200` if object found
      * `404` if object not found


* POST /detail/[model]/[id][0-9]+
    * Post: valid JSON table for corresponding model.

    * Status:
      * `400`: if form posted not valid.
      * `404`: if form posted is valid, but 'ManyToManyField' contains invalid id in corresponding model(car).
      * `201`: if `id` not found in db, automatically create new object by the given info. **Note: the new object will not have the `id` given in the url, system will automatically assign one id to it**.
      * `202`: if `id` found in db, update new object by the given info.


* POST /delete/[model]/[id][0-9]+
    * Post: nothing required

    * Notice:
      * Car: when `car` is deleted, all `user` will automatically remove it from `car_sell` and `favourite`
      * User: when a user is deleted, all `car` in its `car_sell` will be removed, within the same logic as above.   

    * Status:
      * `404`: if object not found
      * `202`: if object found and deleted


* NOTE:
    * All other HTTP request other than those specified above will raise `500` error
    * All unspecified url will raise `404` page not found error

##Example Json Post Format

        //userModel

        {
        "first_name": "new",

        "last_name": "user",

        "user_name": "newuser",

        "password": "12345678",

        "car_sell": [1,2,3],   //optional

        "favourite": [1,2,3]  //optional
        }

        //carModel

        {
        "car_color": "black",

        "car_brand": "Benz",

        "car_model": "G63",

        "description": "This is a car.",

        "price": "9999
        }

## Fixture
