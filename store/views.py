from django.shortcuts import render, redirect
from store.models import *
from .classes import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import F
from django.core.mail import EmailMessage

def check_cart_session(request):
    if 'cart' not in request.session:
        request.session['cart']={}

def add_to_cart(request, client, variety, quantity):
    try:
        Cart.objects.create(fk_client=client, fk_variety=variety, quantity=quantity)
    except IntegrityError:
        existing_record = Cart.objects.get(fk_client = client, fk_variety = variety)
        existing_record.quantity = quantity
        existing_record.save()

def index(request):
    return render(request, 'store/index.html')

def webmarket(request):
    variety = Variety.objects.all()
    category = Category.objects.all()

    if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)
        cart = Cart.objects.filter(fk_client=client)

    else:
        # if user is anonymous, create objects queryset with dict cart session
        check_cart_session(request)
        cart_session = CartSession(request.session.get('cart'))
        cart_session.create_queryset(request)
        cart = cart_session.return_queryset(request)

    if cart is not None:
        for elt in variety :
            for record in cart:
                if elt == record.fk_variety:
                    elt.quantity = record.quantity

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
    if request.method == 'GET':
        if request.user.is_authenticated :
            query = Cart.objects.filter(fk_client=Client.objects.get(user=request.user))

        else:
            # User is anonymous
            check_cart_session(request)
            cart_session = CartSession(request.session.get('cart'))
            cart_session.create_queryset(request)
            query = cart_session.return_queryset(request)

        total_cart = 0
        for product in query:
            product.total = product.quantity * product.fk_variety.price
            total_cart += product.total

        context = {
        "cart" : query,
        "total" : total_cart
        }


        return render(request,'store/cart.html',context)

    elif request.method == "POST":
        id_product = request.POST['cart_object']

        if request.POST['action'] == 'remove':

            if request.user.is_authenticated:
                client = Client.objects.get(user=request.user)
                variety_ref = Variety.objects.get(pk=id_product)

                cart_record = Cart.objects.get(fk_client=client, fk_variety=variety_ref)
                cart_record.delete()
            else:
                request.session['cart'].pop(id_product)
                request.session.modified = True


        elif request.POST['action'] == 'update':
            quantity = request.POST['quantity']
            stock = Variety.objects.get(pk=id_product).stock

            if request.user.is_authenticated:
                client = Client.objects.get(user=request.user)
                variety_ref = Variety.objects.get(pk=id_product)

                cart_record = Cart.objects.get(fk_client=client, fk_variety=variety_ref)

                if int(quantity) <= stock :
                    cart_record.quantity = quantity
                    cart_record.save()

            else:
                if int(quantity) <= stock :
                    request.session['cart'][id_product] = quantity
                    request.session.modified = True

        context = {}

        return JsonResponse(context)

def login_form(request):
    auth_email = request.POST['email'].lower()
    password = request.POST['password']

    if request.POST['choice'] == 'connect':
        try:
            u = User.objects.get(username=auth_email)
            if u.check_password(password):
                user = authenticate(username=auth_email, password=password)
                login(request, user)
                message = "success"

                client = Client.objects.get(user=user)

                check_cart_session(request)
                cart = CartSession(request.session.get('cart'))
                cart.create_queryset(request)
                cart.to_cart_database(request, client, add_to_cart)

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

            client = Client.objects.create(
            user = u,
            phone = request.POST['phone'],
            fk_client_type = ClientType.objects.get(type_client=request.POST['type']),
            fk_adress = adress_form
            )

            user = authenticate(username=auth_email, password=password)
            login(request, user)

            check_cart_session(request)
            cart = CartSession(request.session.get('cart'))
            cart.create_queryset(request)
            cart.to_cart_database(request, client, add_to_cart)

            message = "success"

    context = {"message": message}

    return JsonResponse(context)

def profil(request):

    client = Client.objects.get(user=request.user)

    if request.method == 'GET':
        order = Order.objects.filter(fk_client=client)

        context = {
        "email" :request.user.get_username(),
        "client" : client,
        "order" : order,
        }

        return render(request, 'store/profil.html', context)

    elif request.method == "POST":
        if request.user.check_password(request.POST["password"]):
            if request.POST["action"] == "update_infos":
                request.user.username = request.POST["email"]
                request.user.first_name = request.POST["name"]

                number = request.POST['number']
                street = request.POST['street'].lower()
                cplt = request.POST['cplt'].lower()
                cp = request.POST['cp']
                city =  request.POST['city'].lower()
                try:
                    adress_form = Adress.objects.get(numero = number, rue=street, complement=cplt, code_postal=cp, ville=city)
                except Adress.DoesNotExist:
                    adress_form = Adress.objects.create(numero = number, rue=street, complement=cplt, code_postal=cp, ville=city)

                client.fk_adress = adress_form

                client.phone = request.POST["phone"]

                client.save()
                request.user.save()
                message = "success"

            elif request.POST["action"] == "update_password":
                request.user.set_password(request.POST['newpassword'])
                request.user.save()
                update_session_auth_hash(request, request.user)

                message = "success"

        else:
            message = "incorrect_pass"

        context = {"message": message}

        return JsonResponse(context)

def logout_account(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('store:index')

def delete_account(request):
    if request.user.is_authenticated:
        user = User.objects.get(username = request.user.get_username())
        logout(request)
        user.delete()

    return redirect('store:index')

def adding_in_cart(request):
    id_product = request.POST["product"]
    quantity = request.POST["quantity"]
    variety = Variety.objects.get(pk=id_product)

    if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)
        add_to_cart(request, client, variety, quantity)
    else:
        # User is anonymous
        check_cart_session(request)
        request.session['cart'][id_product] = quantity
        request.session.modified = True

    context = {"message": "ok"}

    return JsonResponse(context)

def email(request):
    admin_mail = User.objects.get(username="admin@farm").email

    email = EmailMessage(
    request.POST['subject'],
    request.POST['message'],
    request.POST['email'],
    [admin_mail,],
    )

    try:
        email.send()
        message = "success"
    except Exception:
        message = "fail"
        
    context = {"message": message}
    return JsonResponse(context)
