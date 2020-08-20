from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Adress(models.Model):
    numero = models.IntegerField()
    rue = models.CharField(max_length=250)
    complement = models.CharField(max_length=250, blank=True, null=True)
    code_postal = models.CharField(max_length=5)
    ville = models.CharField(max_length=100)


class CommandType(models.Model):
    type = models.CharField(max_length=50)


class CommandStatus(models.Model):
    status = models.CharField(max_length=250)


class ClientType(models.Model):
    type_client = models.CharField(max_length=50)


class Category(models.Model):
    name = models.CharField(max_length=250)


class Unity(models.Model):
    type = models.CharField(max_length=50)


class AdminCode(models.Model):
    code = models.IntegerField()


class Product(models.Model):
    name = models.CharField(max_length=250)
    fk_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Variety(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    stock = models.IntegerField()
    image = models.URLField(default="no_url_product")
    fk_unity = models.ForeignKey(Unity, on_delete=models.CASCADE)
    fk_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)


class Day(models.Model):
    name = models.CharField(max_length=50)


class TimeSlot(models.Model):
    fk_day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    fk_command_type = models.ForeignKey(CommandType, on_delete=models.CASCADE)
    max_command = models.IntegerField()


class CollectLocation(models.Model):
    name = models.CharField(max_length=250)
    fk_adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    fk_command_type = models.ForeignKey(CommandType, on_delete=models.CASCADE)
    schedule = models.ManyToManyField(TimeSlot, through='DirectWithdrawal')

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_adress','fk_command_type'],
        name='unicque_collect_location')
        ]


class Locker(models.Model):
    number = models.IntegerField()
    disponibility = models.BooleanField(default=True)
    secret_code = models.IntegerField()
    fk_collect_location = models.ForeignKey(CollectLocation, on_delete=models.CASCADE)
    fk_admin_code = models.ForeignKey(AdminCode, on_delete=models.CASCADE)


class Delivery(models.Model):
    instruction = models.CharField(max_length=250)
    fk_time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)


class DirectWithdrawal(models.Model):
    fk_collect_location = models.ForeignKey(CollectLocation, on_delete=models.CASCADE)
    fk_time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_collect_location','fk_time_slot'],
        name='unique_direct_withdrawal')
        ]


class Client(User):
    phone = models.CharField(max_length=256, blank=True, null=True)
    fk_client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE)
    fk_adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    name_restaurant = models.CharField(max_length=250, blank=True, null=True)
    variety = models.ManyToManyField(Variety, through='Cart')


class Cart(models.Model):
    fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    fk_variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_client','fk_variety'],
        name='unique_product_cart')
        ]


class Order(models.Model):
    number = models.IntegerField()
    fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    fk_locker = models.ForeignKey(Locker, on_delete=models.CASCADE, blank=True, null=True)
    fk_direct_withdrawal = models.ForeignKey(DirectWithdrawal, on_delete=models.CASCADE, blank=True, null=True)
    fk_delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, blank=True, null=True)
    historic_status = models.ManyToManyField(CommandStatus, through='Historic')
    variety = models.ManyToManyField(Variety, through='OrderDetail')


class OrderDetail(models.Model):
    fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fk_variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_order','fk_variety'],
        name='unique_product_order')
        ]


class Historic(models.Model):
    fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fk_command_status = models.ForeignKey(CommandStatus, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_order','fk_command_status'],
        name='unique_order_status')
        ]
