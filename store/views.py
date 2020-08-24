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

def login(request):
    email = request.POST['email']
    password = request.POST['password']

    if request.POST['choice'] == 'connect':
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            message = "succes to connect"
        else:
            message = "incorrect id"

    elif request.POST['choice'] == 'create':
        name = request.POST['name']
        u = User.objects.filter(email=email)
        if u.exists():
            message = "already exists"
        else:
            User.objects.create_user(name, email, password)

            number = request.POST['number']
            street = request.POST['street']
            cp = request.POST['cp']
            city =  request.POST['city']

            adress_form = Adress.objects.filter(numero = number, rue=street, code_postal=cp, ville=city)
            if not adress_form.exists():
                Adress.objects.create(numero = number, rue=street, code_postal=cp, ville=city)

            Client.objects.create(
            user = User.objects.get(email=email),
            phone = request.POST['phone'],
            fk_client_type = ClientType.objects.get(type_client=request.POST['type']),
            fk_adress = Adress.objects.get(numero = number, rue=street, code_postal=cp, ville=city)
            )

            message = "new client created"

    print(message)
    context = {"message": message}

    return JsonResponse(context)
