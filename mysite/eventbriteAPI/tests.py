


import unittest
from django.test.client import Client
from django.core.urlresolvers import reverse

class ViewsTestCase(unittest.TestCase):
    #setting up client
    def setUp(self):
        self.client = Client()
    #Test for Home page
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    #test for getting event list page when no data is sent as part of GET request
    def test_event_list_with_no_data_in_get(self):
        response =self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)

    #test for getting event list page when no category is sent as part of GET request
    def test_event_list_no_category(self):
        response =self.client.get(reverse('event_list'),{'favorite_event_categories': '','page':0})
        self.assertEqual(response.status_code, 200)

    #test for getting event list page when only one category is sent as part of GET request
    def test_event_list_one_category(self):
        response =self.client.get(reverse('event_list'),{'favorite_event_categories': '101','page':0})
        self.assertEqual(response.status_code, 200)

    #Rest of the test cases are pretty much intuitive

    def test_event_list_two_category(self):
        response =self.client.get(reverse('event_list'),{'favorite_event_categories': '101','favorite_event_categories': '109','page':0})
        self.assertEqual(response.status_code, 200)


    def test_event_list_three_category(self):
        response =self.client.get(reverse('event_list'),{'favorite_event_categories': '101','favorite_event_categories': '109','favorite_event_categories': '116','page':0})
        self.assertEqual(response.status_code, 200)

    def test_event_list_wrong_categories(self):
        response =self.client.get(reverse('event_list'),{'favorite_event_categories': '999','favorite_event_categories': '-995','favorite_event_categories': '116','page':0})
        self.assertEqual(response.status_code, 200)

    #test for getting events-by-cat page when correct category is sent as part of GET request
    def test_events_by_cat_correct_input(self):
        response =self.client.get(reverse('events_by_cat'),{'categories': '101','page':5})
        self.assertEqual(response.status_code, 200)

    #test for getting events-by-cat page when incorrect category is sent as part of GET request
    def test_events_by_cat_incorrect_input(self):
        response =self.client.get(reverse('events_by_cat'),{'categories': '-563','page':-468})
        self.assertEqual(response.status_code, 200)

