from django.test import TestCase
import json
from .models import *
from django.test import Client

# Create your tests here.


# The fixtures used in the tests can be found in ../demo.json
# but it is not comprehensive, as django will automatically refill all blank columns


# Test to get detail of a user/car, if exists it should render the corresonding
# car, if not, it should render 404 car/user not found error
class TestGetDetail(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    #retrieve an existing car
    def test_carDetailFound(self):
        c = Client()
        response = c.get('/api/v1/detail/car/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 200, 'car': {'car_new': False, 'car_make': 'Benz', 'car_year': 2016, 'id': 1, 'price': 129999, 'car_model': 'G63', 'car_color': 'red', 'car_body_type': 'a', 'description': 'This is a car'}}
        self.assertEqual(result, output)

    #retrieve an existing user
    def test_userDetailFound(self):
        c = Client()
        response = c.get('/api/v1/detail/user/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        result['user'].pop('password', None)
        output = {'status_code': 200, 'user': {'last_name': 'Cat', 'id': 1, 'favourite': [], 'username': 'superCat', 'car_sell': [{'price': 129999, 'car_year': 2016, 'car_body_type': 'a', 'id': 1, 'car_model': 'G63', 'car_make': 'Benz', 'car_color': 'red', 'description': 'This is a car', 'car_new': False}, {'price': 49999, 'car_year': 2016, 'car_body_type': 'a', 'id': 2, 'car_model': 'Cayanne', 'car_make': 'Porsche', 'car_color': 'black', 'description': 'This is a car', 'car_new': False}, {'price': 49999, 'car_year': 2016, 'car_body_type': 'a', 'id': 3, 'car_model': 'X5', 'car_make': 'BMW', 'car_color': 'white', 'description': 'This is a car', 'car_new': False}], 'first_name': 'Hans'}}
        self.assertEqual(result, output)

    #retrieve a not existing user
    def test_userDetailNotFound(self):
        c = Client()
        response = c.get('/api/v1/detail/user/10')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 404, 'message': "User doesn't exist"}
        self.assertEqual(result, output)

    #retrieve a not existing car
    def test_carDetailNotFound(self):
        c = Client()
        response = c.get('/api/v1/detail/car/10')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 404, 'message': "Car doesn't exist"}
        self.assertNotEqual(result, output)

    def tearDown(self):
        pass


# Test a new seller join the forum, and create a car that he want to sell
class sellerDetailTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    # create a new car
    def test_carCreate(self):
        c = Client()
        post_data = {'car_new': 0, 'car_make': 'BMW', 'car_year': 2016, 'price': 9999, 'car_model': 'Unknown', 'car_color': 'grey', 'car_body_type': 'a', 'description': 'This is a car'}
        response = c.post('/api/v1/detail/car/5', post_data)
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output ={'car': {'car_body_type': 'a', 'car_color': 'grey', 'car_make': 'BMW', 'car_model': 'Unknown', 'car_new': True, 'car_year': 2016, 'description': 'This is a car', 'id': 5, 'price': 9999}, 'status_code': 202}
        self.assertEqual(output, result)

    #User create account with an existing car in database
    def test_sellerCreate(self):
        # make a post to create the user
        c = Client()
        post_data = {'last_name': '1', 'car_sell': [4], 'password': '12345678', 'username': 'newseller', 'first_name': 'seller'}
        response = c.post('/api/v1/detail/user/6', json.dumps(post_data), 'json')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 201, 'message': "Create Success"}
        self.assertEqual(output, result)
        response = c.get('/api/v1/detail/user/?username=newseller')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        # output = {'user': [{'first_name': 'seller', 'last_name': '1', 'favourite': [], 'username': 'newseller', 'id': 7, 'car_sell': [{'price': 39999, 'description': 'This is a car', 'car_model': 'Q7', 'car_make': 'Audi', 'car_year': 2016, 'car_color': 'red', 'car_new': False, 'car_body_type': 'a', 'id': 4}], 'password': 'pbkdf2_sha256$30000$VjqusDSsR9GW$tXBewpNj1tfZovzbVel51Zj/cPNaHlg82zuCsrMQohM='}], 'status_code': 200}
        self.assertEqual(result['user'][0]['username'], 'newseller')

    def tearDown(self):
        pass

# Test a new buyer join the forum, and tag an existing car that he might want to buy
class buyerDetailTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass


    def test_buyerCreate(self):
        # make a post to create the user
        c = Client()
        post_data = {'last_name': '1', 'favourite': [1], 'password': '12345678', 'username': 'newbuyer', 'first_name': 'buyer'}
        response = c.post('/api/v1/detail/user/6', json.dumps(post_data), 'json')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 201, 'message': "Create Success"}
        self.assertEqual(output, result)

        # make a get request to check if the user is created with the given info
        c = Client()
        response = c.get('/api/v1/detail/user/6')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        # output = {'user': {'id': 6, 'username': 'newbuyer', 'password': 'pbkdf2_sha256$30000$1lAF0C6cO4gH$jwPoD0YzncaHUPMSdjor53jy43nwcpcgymw1BjKVU4M=', 'favourite': [{'id': 1, 'car_color': 'red', 'car_model': 'G63', 'car_body_type': 'a', 'car_new': False, 'car_year': 2016, 'description': 'This is a car', 'car_make': 'Benz', 'price': 129999}], 'last_name': '1', 'first_name': 'buyer', 'car_sell': []}, 'status_code': 200}
        self.assertEqual(result['user']['username'], 'newbuyer')

    def tearDown(self):
        pass

# a user want to modify its information
class userUpdateTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    def test_updateBuyer(self):
        c = Client()
        post_data = {'last_name': '1', 'favourite': [1], 'password': '12345678', 'username': 'newbuyer', 'first_name': 'buyer'}
        response = c.post('/api/v1/detail/user/1', json.dumps(post_data), 'json')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 202, 'message': 'Update Success'}
        self.assertEqual(output, result)
        # response = c.get('/api/v1/detail/user/1')
        # result = response.content.decode('utf-8')
        # result = json.loads(result)
        # output = {'status_code': 200, 'user': {'last_name': '1', 'car_sell': [], 'id': 1, 'password': '12345678', 'user_name': 'newbuyer', 'first_name': 'buyer', 'favourite': [1]}}
        # self.assertEqual(output, result)

# a car is deleted, the car instance will be deleted,
# and all the related user's car list will be modified (remove the removed car)
class carDeleteTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    def test_carDelete(self):
        # delete the user
        c = Client()
        response = c.post('/api/v1/delete/car/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 202, 'message': 'Delete Success'}
        self.assertEqual(output, result)

        # the buyer usually has two tagged car [1,2] now it has only [2]
        response = c.get('/api/v1/detail/user/2')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'user': {'first_name': 'buyer', 'id': 2, 'password': 'pbkdf2_sha256$30000$Jmxi4bhUgfy1$jhqFIj5WJ3+qM5m3iu0vJFj/iDqG2k7mjBf9kNFWYVM=', 'favourite': [{'id': 2, 'description': 'This is a car', 'car_make': 'Porsche', 'car_year': 2016, 'car_color': 'black', 'car_new': False, 'car_model': 'Cayanne', 'car_body_type': 'a', 'price': 49999}], 'last_name': '2', 'car_sell': [], 'username': 'buyer2'}, 'status_code': 200}
        self.assertEqual(output, result)

# a user can delete the account, which also results in some car removal
# and corresonding list change for all users
class userDeleteTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    def test_buyerDelete(self):
        # delete the buyer
        c = Client()
        response = c.post('/api/v1/delete/user/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 202, 'message': 'Delete Success'}

    def test_sellerDelete(self):
        # delete the seller
        c = Client()
        response = c.post('/api/v1/delete/user/3')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 202, 'message': 'Delete Success'}

        # all the cars he owned now should be removed
        response = c.get('/api/v1/detail/car/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 404, 'message': "Car doesn't exist"}
        self.assertEqual(result, output)

class authTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    # test if correct password, it will login successfully
    def test_login_1(self):
        c = Client()
        post_data = {'username':'superCat', 'password':'12345678'}
        response = c.post('/api/v1/auth/login/', post_data)
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 200)

    # username incorrect
    def test_login_2(self):
        c = Client()
        post_data = {'username':'superCatFake', 'password':'12345678'}
        response = c.post('/api/v1/auth/login/', post_data)
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 404)

    # username exists, but password not match
    def test_login_3(self):
        c = Client()
        post_data = {'username':'superCat', 'password':'123456789'}
        response = c.post('/api/v1/auth/login/', post_data)
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 403)

    # if login success, check status
    def test_check_status_1(self):
        c = Client()
        post_data = {'username':'superCat', 'password':'12345678'}
        response = c.post('/api/v1/auth/login/', post_data)
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 200)

        auth = result["authenticator"]["auth"]
        response = c.post('/api/v1/auth/check_status/', {'auth' : auth})
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 200)

    # wrong auth will return 403
    def test_check_status_2(self):
        c = Client()
        post_data = {'username':'superCat', 'password':'12345678'}
        response = c.post('/api/v1/auth/login/', post_data)
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 200)

        auth = result["authenticator"]["auth"] + "fake"
        response = c.post('/api/v1/auth/check_status/', {'auth' : auth})
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 403)

    def test_logout(self):
        c = Client()
        post_data = {'username':'superCat', 'password':'12345678'}
        response = c.post('/api/v1/auth/login/', post_data)
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 200)

        auth = result["authenticator"]["auth"]
        response = c.post('/api/v1/auth/check_status/', {'auth' : auth})
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 200)

        response = c.post('/api/v1/auth/logout/', {'auth' : auth})
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 202)

        response = c.post('/api/v1/auth/check_status/', {'auth' : auth})
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 403)

class recTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    # test if correct password, it will login successfully
    def test_rec(self):
        c = Client()
        response = c.get('/api/v1/detail/rec/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        self.assertEqual(result['status_code'], 200)
        self.assertEqual(result['rec'][0]['id'], 2)
        self.assertEqual(result['rec'][1]['id'], 3)
