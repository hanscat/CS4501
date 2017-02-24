from django.test import TestCase
import json
from api.models import *
from django.test import Client

# Create your tests here.


# The fixtures used in the tests can be found in ../demo.json
# but it is not comprehensive, as django will automatically refill all blank columns


# Test to get detail of a user/car, if exists it should render the corresonding
# car, if not, it should render 404 car/user not found error
class getDetailTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    #retrieve an existing car
    def test_carDetailFound(self):
        c = Client()
        response = c.get('/api/v1/detail/car/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 200, 'car': {'car_new': False, 'car_make': 'Benz', 'car_year': 2016, 'id': 1, 'price': 9999, 'car_model': 'G63', 'car_color': 'red', 'car_body_type': 'a', 'description': 'This is a car'}}
        self.assertEqual(result, output)

    #retrieve an existing user
    def test_userDetailFound(self):
        c = Client()
        response = c.get('/api/v1/detail/user/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 200, 'user': {'last_name': '1', 'car_sell': [], 'id': 1, 'password': '12345678', 'user_name': 'buyer1', 'first_name': 'buyer', 'favourite': [1, 2]}}
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
        self.assertEqual(result, output)

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
        response = c.post('/api/v1/detail/car/5', json.dumps(post_data), 'json')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 201, 'message': "Create Success"}
        self.assertEqual(output, result)

    #User create account with an existing car in database
    def test_sellerCreate(self):
        # make a post to create the user
        c = Client()
        post_data = {'last_name': '1', 'car_sell': [4], 'password': '12345678', 'user_name': 'newseller', 'first_name': 'seller'}
        response = c.post('/api/v1/detail/user/6', json.dumps(post_data), 'json')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 201, 'message': "Create Success"}
        self.assertEqual(output, result)
        response = c.get('/api/v1/detail/user/?user_name=newseller')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 200, 'user': [{'last_name': '1', 'car_sell': [4], 'id': 7, 'password': '12345678', 'user_name': 'newseller', 'first_name': 'seller', 'favourite': []}]}
        self.assertEqual(result, output)

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
        post_data = {'last_name': '1', 'favourite': [1], 'password': '12345678', 'user_name': 'newbuyer', 'first_name': 'buyer'}
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
        output = {'status_code': 200, 'user': {'last_name': '1', 'car_sell': [], 'id': 6, 'password': '12345678', 'user_name': 'newbuyer', 'first_name': 'buyer', 'favourite': [1]}}
        self.assertEqual(result, output)

    def tearDown(self):
        pass

# a user want to modify its information
class userUpdateTest(TestCase):
    fixtures = ['demo.json']

    def setUp(self):
        pass

    def test_updateBuyer(self):
        c = Client()
        post_data = {'last_name': '1', 'favourite': [1], 'password': '12345678', 'user_name': 'newbuyer', 'first_name': 'buyer'}
        response = c.post('/api/v1/detail/user/1', json.dumps(post_data), 'json')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 202, 'message': 'Update Success'}
        self.assertEqual(output, result)
        response = c.get('/api/v1/detail/user/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 200, 'user': {'last_name': '1', 'car_sell': [], 'id': 1, 'password': '12345678', 'user_name': 'newbuyer', 'first_name': 'buyer', 'favourite': [1]}}
        self.assertEqual(output, result)

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
        response = c.get('/api/v1/detail/user/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 200, 'user': {'last_name': '1', 'car_sell': [], 'id': 1, 'password': '12345678', 'user_name': 'buyer1', 'first_name': 'buyer', 'favourite': [2]}}
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

        # also those deleted cars shall no longer present in any users list as well
        response = c.get('/api/v1/detail/user/1')
        result = response.content.decode('utf-8')
        result = json.loads(result)
        output = {'status_code': 200, 'user': {'last_name': '1', 'car_sell': [], 'id': 1, 'password': '12345678', 'user_name': 'buyer1', 'first_name': 'buyer', 'favourite': [2]}}
        self.assertEqual(output, result)
