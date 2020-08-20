from store.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client as C
from store.management.commands.create_data import *

# Create your tests here.
class IndexTestCase(TestCase):
    def test_index(self):
        c = C()
        response = c.get(reverse("store:index"))
        self.assertEqual(response.status_code, 200)

class WebmarketTestCase(TestCase):
    def test_index(self):
        c = C()
        response = c.get(reverse("store:webmarket"))
        self.assertEqual(response.status_code, 200)

class MarketplaceTestCase(TestCase):
    def test_index(self):
        c = C()
        response = c.get(reverse("store:marketplaces"))
        self.assertEqual(response.status_code, 200)

class CartTestCase(TestCase):
    def test_index(self):
        c = C()
        response = c.get(reverse("store:cart"))
        self.assertEqual(response.status_code, 200)

class FarmdataTestCase(TestCase):

    def test_database_attributes(self):
        fake_database = Database()
        self.assertIsInstance(fake_database, Database)
        self.assertIsInstance(fake_database.unity, list)
        self.assertIsInstance(fake_database.adress, list)
        self.assertIsInstance(fake_database.product, dict)

    def test_insert_data(self):
        fake_database = Database()
        fake_database.fill_database()
        self.assertEqual(len(Adress.objects.all()), len(fake_database.adress))
        self.assertEqual(len(CommandType.objects.all()), len(fake_database.command_type))
        self.assertEqual(len(CommandStatus.objects.all()), len(fake_database.command_status))
        self.assertEqual(len(ClientType.objects.all()), len(fake_database.client_type))
        self.assertEqual(len(Unity.objects.all()), len(fake_database.unity))
        self.assertEqual(len(Day.objects.all()), len(fake_database.day))
        self.assertEqual(len(TimeSlot.objects.all()), len(fake_database.time))
        self.assertEqual(len(CollectLocation.objects.all()), len(fake_database.emplacement_retrait))
        self.assertEqual(len(Locker.objects.all()), len(fake_database.locker))
        self.assertEqual(len(DirectWithdrawal.objects.all()), len(fake_database.withdrawal))

        nb_category = 0
        nb_product = 0
        nb_variety = 0
        for category_dict, value in fake_database.product.items():
            nb_category+=1
            for product in value:
                nb_product +=1
                nb_variety += len(product.get("variety_list"))
        self.assertEqual(len(Category.objects.all()), nb_category)
        self.assertEqual(len(Product.objects.all()), nb_product)
        self.assertEqual(len(Variety.objects.all()), nb_variety)
