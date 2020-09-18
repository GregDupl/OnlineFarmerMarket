from store.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client as C
from store.management.commands.create_data import *
import datetime

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
    fake_variety = Variety.objects.create(name="fake_name",price=1,stock=20,fk_unity=fake_unity,fk_product=fake_product)
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
        MinimumCommand.objects.create(amount=15)
        c = C()
        c.login(username='fake@mail.com', password='password')
        response = c.get(reverse("store:cart"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_get(self):
        MinimumCommand.objects.create(amount=15)
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

    def test_update_infos(self):
        c = C()
        c.login(username='fake@mail.com', password='password')
        user = User.objects.get(username='fake@mail.com')
        initial_city = Client.objects.get(user=user).fk_adress.ville
        response = c.post(reverse("store:account"), {
        "action" : "update_infos",
        "email" : 'fake@mail.com',
        "name" : 'name',
        "phone": '',
        "number": 1,
        "street" : 'newstreet',
        "cplt" : 'cplt',
        "cp" : 95000,
        "city" : 'newcity',
        "password" : 'password'
        })
        new_city = Client.objects.get(user=user).fk_adress.ville
        self.assertEqual('new'+initial_city, new_city)
        self.assertEqual(response.status_code, 200)

    def test_update_pass(self):
        c = C()
        c.login(username='fake@mail.com', password='password')
        response = c.post(reverse("store:account"), {
        "action" : "update_password",
        "newpassword" : "newpass",
        "password": "password"
        })
        user = User.objects.get(username='fake@mail.com')
        self.assertEqual(user.check_password("newpass"), True)
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

class EmailTestCase(TestCase):
    def test_send_email(self):
        User.objects.create(username="admin@farm", email="admin@mail.com", password="password")
        c = C()
        response = c.post(reverse("store:contact"), {
        "email":"fake_email",
        "subject":"fake_subject",
        "message":"fake_message"
        })
        self.assertEqual(response.status_code, 200)

class CommandTestCase(TestCase):
    def setUp(self):
        fake_dataset()

    def test_command_whitout_referer(self):
        c = C()
        c.login(username='fake@mail.com', password='password')
        response = c.get(reverse("store:command"))
        self.assertEqual(response.status_code, 302)

class ReservationTestCase(TestCase):
    def test_reservation(self):
        fake_variety, fake_client = fake_dataset()
        c = C()
        c.login(username='fake@mail.com', password='password')
        fake_cart = Cart.objects.create(fk_client = fake_client, fk_variety = fake_variety, quantity=15)
        response = c.post(reverse("store:reservation"), {
        "button":True
        })
        self.assertEqual(response.status_code, 200)

class CommandValidationTestCase(TestCase):
    def test_validation_commande(self):
        fake_variety, fake_client = fake_dataset()
        c = C()
        c.login(username='fake@mail.com', password='password')
        fake_cart = Cart.objects.create(fk_client = fake_client, fk_variety = fake_variety, quantity=15)
        ClientReadyToCommand.objects.create(fk_client=fake_client, validation_date=datetime.datetime.now())
        fake_type = CommandType.objects.create(type="fake_type")
        fake_day = Day.objects.create(name="lundi")
        fake_time = TimeSlot.objects.create(fk_day=fake_day, start_time=datetime.time(8,30,00), end_time=datetime.time(11,30,00), fk_command_type=fake_type)
        fake_collect = CollectLocation.objects.create(name="fake_name",fk_adress=Adress.objects.get(ville='city'), fk_command_type=fake_type)
        fake_withdrawal = DirectWithdrawal.objects.create(fk_collect_location=fake_collect, fk_time_slot=fake_time)

        initial = Order.objects.count()
        response = c.post(reverse("store:valid"), {
        "choice":"withdrawal",
        "option_withdrawal":fake_withdrawal.pk,
        })
        new=Order.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(new, initial+1)


class RemoveOrderTestCase(TestCase):
    def test_remove_order(self):
        fake_variety, fake_client = fake_dataset()
        c = C()
        c.login(username='fake@mail.com', password='password')
        fake_type = CommandType.objects.create(type="fake_type")
        fake_day = Day.objects.create(name="lundi")
        fake_time = TimeSlot.objects.create(fk_day=fake_day, start_time=datetime.time(8,30,00), end_time=datetime.time(11,30,00), fk_command_type=fake_type)
        fake_collect = CollectLocation.objects.create(name="fake_name",fk_adress=Adress.objects.get(ville='city'), fk_command_type=fake_type)
        fake_withdrawal = DirectWithdrawal.objects.create(fk_collect_location=fake_collect, fk_time_slot=fake_time)

        fake_order = Order.objects.create(fk_client = fake_client, fk_direct_withdrawal=fake_withdrawal)
        detail = OrderDetail.objects.create(fk_order = fake_order, fk_variety=fake_variety, quantity=15)
        historic = OrderHistoric.objects.create(fk_order=fake_order, date_creation=datetime.datetime.now())

        initial_order = Order.objects.filter(fk_client=fake_client).count()
        initial_detail = OrderDetail.objects.filter(fk_order=fake_order).count()
        initial_historic = OrderHistoric.objects.filter(fk_order=fake_order).count()
        initial_stock = fake_variety.stock

        response = c.post(reverse("store:remove"),{
        "id" : fake_order.pk
        })

        new_order = Order.objects.filter(fk_client=fake_client).count()
        new_detail = OrderDetail.objects.filter(fk_order=fake_order).count()
        new_historic = OrderHistoric.objects.filter(fk_order=fake_order).count()
        new_stock = Variety.objects.get(name="fake_name").stock

        self.assertEqual(new_order, initial_order-1)
        self.assertEqual(new_detail, initial_detail-1)
        self.assertEqual(new_historic, initial_historic-1)
        self.assertEqual(new_stock, initial_stock+15)
