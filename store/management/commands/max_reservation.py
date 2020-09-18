from django.core.management.base import BaseCommand
from store.models import *
from django.db.models import F
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        for obj_ready in ClientReadyToCommand.objects.filter(block=False) :
            client = obj_ready.fk_client
            delta = datetime.datetime.now() - obj_ready.validation_date
            if delta.seconds > 120 :
                try:
                    # remove from ClientReadyToCommand
                    ClientReadyToCommand.objects.get(fk_client=client, block=False).delete()

                    # adding quantities in variety stock
                    cart = Cart.objects.filter(fk_client = client)
                    for obj_cart in cart :
                        variety = obj_cart.fk_variety
                        variety.stock = F('stock') + obj_cart.quantity
                        variety.save()

                except ClientReadyToCommand.DoesNotExist:
                    pass
