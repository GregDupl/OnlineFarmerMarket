from store.models import *
from django.db.models import F


class CartObject:
    """Create a product's cart object with variety and quantity attributes """

    def __init__(self, variety, quantity):
        self.fk_variety = variety
        self.quantity = int(quantity)


class CartSession(CartObject, Variety):
    """To create an cart object with request.session['cart'] of
    the anonymous user. The object can call several methods to create a list
    of cart item object in the manner of a queryset
    """

    def __init__(self, dict):
        self.data = dict

    def create_queryset(self, request):
        self.objects = []
        for key, value in self.data.items():
            fk_variety = Variety.objects.get(pk=key)
            quantity = value
            cart_item = CartObject(fk_variety, quantity)
            self.objects.append(cart_item)

    def return_queryset(self, request):
        return self.objects

    def update(self, request):
        for obj in self.objects:
            key = str(obj.fk_variety.pk)
            if obj.fk_variety.stock == 0 or obj.fk_variety.available is False:
                self.data.pop(key)
                self.objects.remove(obj)

            elif obj.quantity > obj.fk_variety.stock:
                obj.quantity = obj.fk_variety.stock
                self.data[key] = str(obj.quantity)

        return self.data

    def to_cart_database(self, request, client, add):
        for object in self.objects:
            variety = object.fk_variety
            quantity = object.quantity
            add(request, client, variety, quantity)


class UserCart:
    '''Create an object with queryset of client and cart from database.
    An object can call two methods, to calcul a total and to unsave
    product of the cart's client in the database
    '''

    def __init__(self, client):
        self.client = client
        self.cart_queryset = Cart.objects.filter(fk_client=self.client)

    def total(self):
        total_cart = 0
        for product in self.cart_queryset:
            product.total = product.quantity * product.fk_variety.price
            total_cart += product.total
        return total_cart, self.cart_queryset

    def unsave(self):
        for obj in self.cart_queryset:
            variety = obj.fk_variety
            variety.stock = F("stock") + obj.quantity
            variety.save()
