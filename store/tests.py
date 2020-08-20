from store.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client


# Create your tests here.
class IndexTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get(reverse("store:index"))
        self.assertEqual(response.status_code, 200)

class WebmarketTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get(reverse("store:webmarket"))
        self.assertEqual(response.status_code, 200)

class MarketplaceTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get(reverse("store:marketplaces"))
        self.assertEqual(response.status_code, 200)

class CartTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get(reverse("store:cart"))
        self.assertEqual(response.status_code, 200)
