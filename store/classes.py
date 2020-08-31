from store.models import *

class CartObject():
    """Create a cart object with variety and quantity attributes """

    def __init__(self, variety, quantity):
        self.fk_variety = variety
        self.quantity = int(quantity)


class CartSession(CartObject, Variety):
    """To create an object with methods based on request.session['cart']"""

    def __init__(self, dict):
        self.data = dict

    def create_queryset(self, request):
        self.objects = []
        for key, value in self.data.items():
            fk_variety = Variety.objects.get(pk=key)
            quantity = value
            cart_item = CartObject(fk_variety,quantity)
            self.objects.append(cart_item)

    def return_queryset(self, request):
            return self.objects

    def to_cart_database(self, request, client, add):
        for object in self.objects:
            variety = object.fk_variety
            quantity = object.quantity
            add(request,client,variety,quantity)
