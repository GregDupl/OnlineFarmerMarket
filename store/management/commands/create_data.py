from django.core.management.base import BaseCommand, CommandError
from store.models import *
from .initial_data import *

class Database():
    """Class to adding data in Database for a first utilisation"""

    def __init__(self):
        self.unity = DATA["unity_product"]
        self.command_type = DATA["command_type"]
        self.command_status = DATA["command_status"]
        self.client_type = DATA["client_type"]
        self.admin_code = 123456
        self.adress = DATA["adresse"]
        self.day = DATA["day"]
        self.time =DATA["time"]
        self.emplacement_retrait = DATA["emplacement_retrait"]
        self.withdrawal = DATA["withdrawal"]
        self.locker = DATA["locker_data"]
        self.product = DATA["product_farm"]

    def insert_unity(self):
        for elt in self.unity:
            Unity.objects.create(type = elt)

    def insert_command_type(self):
        for elt in self.command_type:
            CommandType.objects.create(type = elt)

    def insert_command_status(self):
        for item in self.command_status:
            CommandStatus.objects.create(status = item)

    def insert_client_type(self):
        for item in self.client_type:
            ClientType.objects.create(type_client = item)

    def insert_admin_code(self):
        AdminCode.objects.create(code = self.admin_code)

    def insert_adress(self):
        for elt in self.adress:
            Adress.objects.create(
            numero = elt[0],
            rue = elt[1],
            code_postal = elt[2],
            ville = elt[3]
            )

    def insert_day(self):
        for elt in self.day:
            Day.objects.create(name = elt)

    def insert_time(self):
        for elt in self.time:
            TimeSlot.objects.create(
            fk_day = Day.objects.get(name=elt[0]),
            start_time = elt[1],
            end_time = elt[2],
            fk_command_type = CommandType.objects.get(pk=elt[3]),
            )
    def insert_emplacement_retrait(self):
        for elt in self.emplacement_retrait:
            CollectLocation.objects.create(
            name = elt[0],
            fk_adress = Adress.objects.get(pk=elt[1]),
            fk_command_type = CommandType.objects.get(pk=elt[2])
            )

    def insert_withdrawal(self):
        for elt in self.withdrawal:
            DirectWithdrawal.objects.create(
            fk_collect_location = CollectLocation.objects.get(pk=elt[0]),
            fk_time_slot = TimeSlot.objects.get(pk=elt[1]),
            )

    def insert_locker(self):
        for elt in self.locker:
            Locker.objects.create(
            number = elt[0],
            secret_code = elt[1],
            fk_collect_location = CollectLocation.objects.get(pk=elt[2]),
            fk_admin_code = AdminCode.objects.get(pk=elt[3]),
            )

    def insert_product(self):
        for key, list in self.product.items():
            Category.objects.create(name = key)
            categ = Category.objects.get(name=key)

            for dict in list:
                name_product = dict.get("name")

                Product.objects.create(name = name_product, fk_category = categ)

                list_variety = dict.get("variety_list")
                for elt in list_variety:
                    Variety.objects.create(
                    name = elt[0],
                    price = elt[1],
                    stock = elt[2],
                    fk_unity = Unity.objects.get(type=elt[3]),
                    fk_product = Product.objects.get(name = name_product)
                    )

    def fill_database(self):
        self.insert_adress()
        self.insert_command_type()
        self.insert_command_status()
        self.insert_client_type()
        self.insert_unity()
        self.insert_admin_code()
        self.insert_day()
        self.insert_time()
        self.insert_emplacement_retrait()
        self.insert_locker()
        self.insert_withdrawal()
        self.insert_product()


class Command(BaseCommand):

    def handle(self, *args, **options):
        farm_database = Database()
        farm_database.fill_database()
