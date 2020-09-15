from store.models import *
from django.db.models import F
import datetime

ready_list = ClientReadyToCommand.objects.all()

for obj_ready in ready_list :
    if obj_ready.block is False:
        obj_ready.block = True
        client = Client.objects.get(pk=obj_ready.fk_client.pk)
        delta = datetime.datetime.now() - obj_ready.validation_date

        if delta.seconds > 300 :
            # remove from ClientReadyToCommand
            ClientReadyToCommand.objects.delete(obj_ready)

            # adding quantities in variety stock
            cart = Cart.objects.filter(fk_client = client)
            for obj_cart in cart :
                variety = obj_cart.fk_variety
                variety.stock = F('stock') + obj_cart.quantity
                variety.save()
        else:
            obj_ready.block = False
