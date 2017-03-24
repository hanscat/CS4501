from django.test import TestCase, Client
from django.core.urlresolvers import reverse
import unittest, json, time


# project 3 test cases
class TestGetCar(TestCase):
    def setUp(self):  # called before each test in this class
        pass

    # test success of data retrieval with legal keys
    def test_success_response(self):
        response = self.client.get(reverse('carPage', kwargs={'car_id': '1'}))  # assumes car with id 1 is stored in db
        #self.assertContains(response,
         #                   'car_id')  # checks that response contains parameter order list & implicitly checks that                                                 #statuscode is 200
        self.assertEqual(response.status_code, 200)

    # test failure when called with invalid key
    def test_fails_invalid(self):
        response = self.client.get(reverse('carPage', kwargs={'car_id': '0'}))
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        self.assertEquals(jsonResponse["status_code"], 404)

    def test_itemFields(self):
        response = self.client.get(reverse('carPage', kwargs={'car_id': '1'}))
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        # test for every fields of car model
        self.assertEquals(jsonResponse["status_code"], 200)
        self.assertContains(response, 'car_make')
        self.assertContains(response, 'car_model')
        self.assertContains(response, 'car_color')
        self.assertContains(response, 'description')
        self.assertContains(response, 'price')

    def tearDown(self):  #called after each test to mark ending
        pass

class TestGetUser(TestCase):
    def setUp(self):  # called before each test in this class
        pass

    # test success of data retrieval with legal keys
    def test_success_response(self):
        response = self.client.get(reverse('userPage', kwargs={'user_id': '1'}))  # assumes user with id 1 is stored in db
        #self.assertContains(response,
         #                   'user_id')  # checks that response contains parameter order list & implicitly checks that                                                 #statuscode is 200
        self.assertEqual(response.status_code, 200)

    # test failure when no key or invalid key
    def test_fails_invalid(self):
        response = self.client.get(reverse('userPage', kwargs={'user_id': '0'}))
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        self.assertEquals(jsonResponse["status_code"], 404)

    def test_itemFields(self):
        response = self.client.get(reverse('userPage', kwargs={'user_id': '1'}))
        jsonResponse = json.loads(str(response.content, encoding='utf8'))
        # test for every fields of car model
        self.assertEquals(jsonResponse["status_code"], 200)
        self.assertContains(response, 'first_name')
        self.assertContains(response, 'last_name')
        self.assertContains(response, 'user_name')
        self.assertContains(response, 'favourite')
        self.assertContains(response, 'car_sell')

    def tearDown(self):  #called after each test to mark ending
        pass
        # project 4 test cases


# tests login and logout cases, two separate test cases combined into one
class authTestCase(TestCase):
    def setUp(self):  # setUp method is called before each test in this class
        pass  # nothing to set uunpit

    def test_success_response(self):
        response = self.client.post(reverse('loginPage'), {'username': 'hans', 'passwd': 'hans_pwd'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'status')
        self.assertContains(response, 'auth')

    def test_success_can_login(self):
        response = self.client.post(reverse('loginPage'), {'username': 'jerry', 'passwd': 'jerry_pwd'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'status')
        self.assertContains(response, 'auth')
        ret = response.content.decode('utf-8')
        ret = json.loads(ret)
        self.assertEqual(ret['status'], True)

        response = self.client.post(reverse('logoutPage'), {'auth': ret['auth']})
        ret = response.content.decode('utf-8')
        ret = json.loads(ret)
        self.assertEquals(ret['status'], True)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):  # tearDown method is called after each test
        pass


# class createListingTestCase(TestCase):
#     def setUp(self):  # setUp method is called before each test in this class
#         pass
#     def test_success_Creation(self):
#         # login first
#         response = self.client.post(reverse('loginPage'), {'username': 'carFan', 'passwd': '666666'})
#         ret = response.content.decode('utf-8')
#         ret = json.loads(ret)
#         response = self.client.post(reverse('createListingPage'), {"car_color": "red",
#                                                                 "car_make": 'Alfa Romeo',
#                                                                 "car_model": 'Giulia',
#                                                                 "car_year": '2017',
#                                                                 "car_body_type": 'sedan',
#                                                                 "car_new": 'True',
#                                                                 "description": 'great Italian car',
#                                                                 "price": '45999',
#                                                                 "auth": ret['auth']
#                                                                 })
#
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(ret['status'], True)
#
#         response = self.client.post(reverse('logoutPage'), {'auth': ret['auth']})
#     def tearDown(self):  # tearDown method is called after each test
#         pass


# tests account creation
class createAccountTestCase(TestCase):
    def setUp(self):  # setUp method is called before each test in this class
        pass  # nothing to set uunpit

    def test_success_createAccount(self):
        response = self.client.post(reverse('createaccountPage'),
                                    {'username': 'Hans', 'password': 'hans_pwd', 'first_name': 'Hans',
                                     'last_name': 'Zhang', 'email': 'hans@virginia.edu'})
        ret = response.content.decode('utf-8')
        ret = json.loads(ret)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(ret['status'], True)

    def test_success_createFailAccount(self):
        response = self.client.post(reverse('createaccountPage'),
                                    {'username': 'Jerry', 'password': 'jerry_pwd', 'first_name': 'Jerry',
                                     'last_name': 'Sun', 'email': 'jerry@virginia.edu'})
        ret = response.content.decode('utf-8')
        ret = json.loads(ret)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(ret['status'], False)

    def tearDown(self):  # tearDown method is called after each test
        pass
