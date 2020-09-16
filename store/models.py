from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class Adress(models.Model):
    numero = models.IntegerField()
    rue = models.CharField(max_length=250)
    complement = models.CharField(max_length=250, blank=True, null=True)
    code_postal = models.CharField(max_length=5)
    ville = models.CharField(max_length=100)

    def __str__(self):
        title= "{} {} {}, {} {}".format(self.numero, self.rue, self.complement, self.code_postal, self.ville)
        return title

    class Meta:
        verbose_name = 'Adresse enregistrée'
        verbose_name_plural = 'Adresses enregistrées'

class CommandType(models.Model):
    type = models.CharField(max_length=50)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Type de commande'
        verbose_name_plural = 'Types de commande'



class ClientType(models.Model):
    type_client = models.CharField(max_length=50)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.type_client

    class Meta:
        verbose_name = 'Type de clientèle'
        verbose_name_plural = 'Types de clientèle'

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Catégorie de produit'
        verbose_name_plural = 'Catégories de produit'

class Unity(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Unité'
        verbose_name_plural = 'Unités'


class AdminCode(models.Model):
    code = models.IntegerField()

    def __str__(self):
        return str(self.code)

    class Meta:
        verbose_name = 'Admin code lockers'
        verbose_name_plural = 'admin code lockers'


class Product(models.Model):
    name = models.CharField(max_length=250)
    fk_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'

class Variety(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="medias_variety/")
    fk_unity = models.ForeignKey(Unity, on_delete=models.CASCADE)
    fk_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Variété produit'
        verbose_name_plural = 'Variétés produit'

class Day(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Jour'
        verbose_name_plural = 'Jours'


class TimeSlot(models.Model):
    fk_day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    fk_command_type = models.ForeignKey(CommandType, on_delete=models.CASCADE,
    limit_choices_to=Q(type="withdrawal") | Q(type="delivery"))

    def __str__(self):
        title = "{} de {} à {} - {}".format(
        self.fk_day, self.start_time, self.end_time, self.fk_command_type)
        return title

    class Meta:
        verbose_name = 'Plage horaire'
        verbose_name_plural = 'Plages horaires'

class CollectLocation(models.Model):
    name = models.CharField(max_length=250)
    fk_adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    fk_command_type = models.ForeignKey(CommandType, on_delete=models.CASCADE,
    limit_choices_to=Q(type="withdrawal") | Q(type="locker"))
    schedule = models.ManyToManyField(TimeSlot, through='DirectWithdrawal')

    def __str__(self):
        title = "{} - {} - {}".format(self.name, self.fk_adress, self.fk_command_type)
        return title

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_adress','fk_command_type'],
        name='unicque_collect_location')
        ]
        verbose_name = 'lieu de collecte'
        verbose_name_plural = 'Lieux de collecte'


class Locker(models.Model):
    number = models.IntegerField()
    disponibility = models.BooleanField(default=True)
    secret_code = models.IntegerField()
    fk_collect_location = models.ForeignKey(
    CollectLocation, on_delete=models.CASCADE,
    limit_choices_to={"fk_command_type":2}
    )
    fk_admin_code = models.ForeignKey(AdminCode, on_delete=models.CASCADE)

    def __str__(self):
        title = "{} - {}".format(self.number, self.fk_collect_location)
        return title

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['number','fk_collect_location'],
        name='unicque_locker_location')
        ]
        verbose_name = 'Casier click&collect'
        verbose_name_plural = 'Casiers click&collect'


class DeliverySlots(models.Model):
    fk_time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,
    limit_choices_to={"fk_command_type":3}
    )
    max_command = models.PositiveIntegerField()
    delivery_area = models.CharField(max_length=250)


class Delivery(models.Model):
    instruction = models.TextField()
    fk_delivery_slot = models.ForeignKey(DeliverySlots, on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = 'Livraison'
        verbose_name_plural = 'Livraisons'


class DirectWithdrawal(models.Model):
    fk_collect_location = models.ForeignKey(CollectLocation, on_delete=models.CASCADE,
    limit_choices_to={"fk_command_type":1})
    fk_time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,
    limit_choices_to={"fk_command_type":1})
    max_command = models.PositiveIntegerField(default=50)

    def __str__(self):
        return str(self.fk_collect_location)

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_collect_location','fk_time_slot'],
        name='unique_direct_withdrawal')
        ]
        verbose_name = 'Emplacement de retrait en direct'
        verbose_name_plural = 'Emplacements de retrait en direct'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=256, blank=True, null=True)
    fk_client_type = models.ForeignKey(ClientType, on_delete=models.CASCADE)
    fk_adress = models.ForeignKey(Adress, on_delete=models.CASCADE)
    variety = models.ManyToManyField(Variety, through='Cart')

    def __str__(self):
        return str(self.user.first_name)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Cart(models.Model):
    fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    fk_variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_client','fk_variety'],
        name='unique_product_cart')
        ]
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'


class Order(models.Model):
    fk_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    fk_locker = models.OneToOneField(Locker, on_delete=models.CASCADE, blank=True, null=True)
    fk_direct_withdrawal = models.ForeignKey(DirectWithdrawal, on_delete=models.CASCADE, blank=True, null=True)
    fk_delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, blank=True, null=True)
    variety = models.ManyToManyField(Variety, through='OrderDetail')

    def __str__(self):
        return str("{} - {}".format(self.fk_client, self.number))

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

class OrderHistoric(models.Model):
    fk_order = models.OneToOneField(Order, on_delete=models.CASCADE)
    date_creation = models.DateField(auto_now_add=True)
    date_end = models.DateField(null=True)
    date_cancellation = models.DateField(null=True)


class OrderDetail(models.Model):
    fk_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fk_variety = models.ForeignKey(Variety, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.fk_order)

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['fk_order','fk_variety'],
        name='unique_product_order')
        ]
        verbose_name = 'Détail de commande'
        verbose_name_plural = 'Détails de commande'



class ClientReadyToCommand(models.Model):
    fk_client = models.OneToOneField(Client, on_delete=models.CASCADE)
    validation_date = models.DateTimeField()
    block = models.BooleanField(default=False)

    def __str__(self):
        return str(self.fk_client)

class MinimumCommand(models.Model):
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.amount)

class MessageToClient(models.Model):
    message = models.TextField()

    def __str__(self):
        return str(self.message)
