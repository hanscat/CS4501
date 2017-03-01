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