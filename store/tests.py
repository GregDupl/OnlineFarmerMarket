from store.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client as C
from store.management.commands.create_data import *

def fake_dataset():
    u = User.objects.create_user(username='fake@mail.com', password='password', first_name='name')
    fake_adress = Adress.objects.create(numero = 1, rue='street', complement='cplt', code_postal=95000, ville='city')
    type = ClientType.objects.create(type_client="parctiulier")
    fake_client = Client.objects.create(
    user = u,
    phone = '',
    fk_client_type = ClientType.objects.get(type_client="parctiulier"),
    fk_adress = fake_adress
    )
    fake_unity = Unity.objects.create(type="fake_type")
    fake_category = Category.objects.create(name="fake_category")
    fake_product = Product.objects.create(name="fake_product", fk_category=fake_category)
    fake_variety = Variety.objects.create(name="fake_name",price=1,stock=10,fk_unity=fake_unity,fk_product=fake_product)
    return fake_variety, fake_client

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
    def test_authenticated_get(self):
        fake_dataset()
        c = C()
        c.login(username='fake@mail.com', password='password')
        response = c.get(reverse("store:cart"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_get(self):
        c = C()
        response = c.get(reverse("store:cart"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_post_remove(self):
        fake_variety, fake_client = fake_dataset()
        c = C()
        c.login(username='fake@mail.com', password='password')
        fake_cart = Cart.objects.create(fk_client = fake_client, fk_variety = fake_variety, quantity=5)
        initial = Cart.objects.count()
        response = c.post(reverse("store:cart"), {'action':'remove','cart_object':fake_variety.pk})
        new = Cart.objects.count()
        self.assertEqual(new,initial-1)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_post_update(self):
        fake_variety, fake_client = fake_dataset()
        c = C()
        c.login(username='fake@mail.com', password='password')
        initial_cart = Cart.objects.create(fk_client = fake_client, fk_variety = fake_variety, quantity=5)
        response = c.post(reverse("store:cart"), {'action':'update','cart_object':fake_variety.pk, 'quantity': 3})
        new_cart = Cart.objects.get(fk_client = fake_client, fk_variety = fake_variety)
        self.assertEqual(new_cart.quantity,initial_cart.quantity-2)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_post_remove(self):
        fake_variety, fake_client = fake_dataset()
        c = C()
        session = c.session
        session['cart'] = {}
        session['cart'][fake_variety.pk] = "5"
        session.save()
        response = c.post(reverse("store:cart"), {'action':'remove','cart_object':fake_variety.pk})
        self.assertEqual(c.session['cart'], {})
        self.assertEqual(response.status_code, 200)

    def test_anonymous_post_update(self):
        fake_variety, fake_client = fake_dataset()
        c = C()
        session = c.session
        session['cart'] = {}
        session['cart'][fake_variety.pk] = "5"
        session.save()
        response = c.post(reverse("store:cart"), {'action':'update','cart_object':fake_variety.pk, "quantity" : "3"})
        self.assertEqual(c.session['cart'], {str(fake_variety.pk):"3"})
        self.assertEqual(response.status_code, 200)


class AddCart(TestCase):
    def setUp(self):
        fake_dataset()

    def test_authenticated_user(self):
        c = C()
        c.login(username='fake@mail.com', password='password')
        id_product = Variety.objects.get(name="fake_name").pk
        initial_number = Cart.objects.count()
        response = c.post(reverse("store:adding_cart"), {"product" : id_product, "quantity" : 2})
        new_number = Cart.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_number,initial_number+1)

    def test_anonymous_user(self):
        c = C()
        id_product = Variety.objects.get(name="fake_name").pk
        response = c.post(reverse("store:adding_cart"), {"product" : id_product, "quantity" : 2})
        session = c.session
        self.assertEqual(session['cart'], {str(id_product) : "2"})
        self.assertEqual(response.status_code, 200)


class AFarmdataTestCase(TestCase):
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


class ProfilTestCase(TestCase):
    def setUp(self):
        fake_dataset()

    def test_profil(self):
        c = C()
        c.login(username='fake@mail.com', password='password')
        response = c.get(reverse("store:account"))
        self.assertEqual(response.status_code, 200)

class DeconnectTestCase(TestCase):
    def setUp(self):
        fake_dataset()

    def test_deconnect(self):
        c = C()
        c.login(username='fake@mail.com', password='password')
        response = c.get(reverse("store:logout"))
        self.assertEqual(response.status_code, 302)

class DeleteUserTestCase(TestCase):
    def setUp(self):
        fake_dataset()

    def test_delete_user(self):
        initial_number = User.objects.count()
        c = C()
        c.login(username='fake@mail.com', password='password')
        response = c.get(reverse("store:delete_account"))
        new_number = User.objects.count()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(initial_number-1, new_number)
