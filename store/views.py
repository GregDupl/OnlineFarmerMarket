from django.shortcuts import render
from store.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request, 'store/index.html')

def webmarket(request):
    variety = Variety.objects.all()
    category = Category.objects.all()

    context = {
    "catalog" : variety,
    "filter" : category
    }

    return render(request,'store/webmarket.html', context)


def marketplaces(request):
    places = DirectWithdrawal.objects.all()
    locker = CollectLocation.objects.filter(fk_command_type__type = "locker")
    restaurant = TimeSlot.objects.filter(fk_command_type__type = "delivery")

    context = {
    "places" : places,
    "locker" : locker,
    "restaurant": restaurant
    }

    return render(request,'store/marketplaces.html', context)

def cart(request):
    return render(request,'store/cart.html')

def login_form(request):
    auth_email = request.POST['email'].lower()
    password = request.POST['password']

    if request.POST['choice'] == 'connect':
        try:
            u = User.objects.get(username=auth_email)
            if u.check_password(password):
                user = authenticate(username=auth_email, password=password)
                login(request, user)
                message = "succes to connect"
            else:
                message = "incorect password"

        except User.DoesNotExist:
            message = "incorrect id"

    elif request.POST['choice'] == 'create':
        name = request.POST['name']

        try:
            u = User.objects.get(username=auth_email)
            message = "already exists"
        except User.DoesNotExist:
            u = User.objects.create_user(username=auth_email, password=password, first_name=name)

            number = request.POST['number']
            street = request.POST['street'].lower()
            cplt = request.POST['cplt'].lower()
            cp = request.POST['cp']
            city =  request.POST['city'].lower()

            try:
                adress_form = Adress.objects.get(numero = number, rue=street, complement=cplt, code_postal=cp, ville=city)
            except Adress.DoesNotExist:
                adress_form = Adress.objects.create(numero = number, rue=street, complement=cplt, code_postal=cp, ville=city)

            Client.objects.create(
            user = u,
            phone = request.POST['phone'],
            fk_client_type = ClientType.objects.get(type_client=request.POST['type']),
            fk_adress = adress_form
            )

            message = "new client created"

    print(message)
    context = {"message": message}

    return JsonResponse(context)
