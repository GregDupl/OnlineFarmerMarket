from django.shortcuts import render, redirect
from store.models import *
from .classes import *
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash
)
from django.http import JsonResponse
from django.db import IntegrityError
from django.db.models import F
from django.core.mail import EmailMessage
import datetime
from django.urls import reverse
from django.db import transaction
from django.views.decorators.cache import never_cache

##################


def check_cart_session(request):
    """Check if user has a cart dictionary
    in request.session and create one if not
    """

    if "cart" not in request.session:
        request.session["cart"] = {}


def add_to_cart(request, client, variety, quantity):
    """Add a variety in user cart. If intergity error,
    not create but change quantity of the existing record in cart user
    """

    try:
        Cart.objects.create(
            fk_client=client,
            fk_variety=variety,
            quantity=quantity
        )
    except IntegrityError:
        existing_record = Cart.objects.get(
            fk_client=client,
            fk_variety=variety
        )
        existing_record.quantity = quantity
        existing_record.save()


def update_cart_values(request, client):
    """Compare cart objects with stock and availability of the referenced
    variety. Delete or update depending these conditions
    """

    for obj in Cart.objects.filter(fk_client=client):
        if obj.fk_variety.stock == 0 or obj.fk_variety.available is False:
            obj.delete()

        elif obj.quantity > obj.fk_variety.stock:
            obj.quantity = obj.fk_variety.stock
            obj.save()


def before(request):
    """If the authenticated user is in ready to command list, delete him
    from this and add quantity of his cart items in the stock of referenced
    variety
    """

    if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)
        try:
            ClientReadyToCommand.objects.get(fk_client=client).delete()
            cart = UserCart(client)
            cart.unsave()
        except ClientReadyToCommand.DoesNotExist:
            pass


##################


def index(request):
    """Load index template"""

    before(request)
    return render(request, "store/index.html")


def webmarket(request):
    """Load catalog of available products of the farm. If user has a cart,
    add quantity on variety referenced
    """

    before(request)

    variety = Variety.objects.filter(available=True)
    category = Category.objects.all()

    if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)

        update_cart_values(request, client)

        cart = Cart.objects.filter(fk_client=client)

    else:
        # if user is anonymous, create objects queryset with dict cart session
        check_cart_session(request)
        cart_session = CartSession(request.session.get("cart"))
        cart_session.create_queryset(request)
        request.session["cart"] = cart_session.update(request)
        cart = cart_session.return_queryset(request)

    if cart is not None:
        for elt in variety:
            for record in cart:
                if elt == record.fk_variety:
                    elt.quantity = record.quantity

    context = {"catalog": variety, "filter": category}

    return render(request, "store/webmarket.html", context)


def marketplaces(request):
    """ Load template to display all market places of the farm """

    before(request)
    places = DirectWithdrawal.objects.all()
    locker = CollectLocation.objects.filter(fk_command_type__type="locker")
    restaurant = TimeSlot.objects.filter(fk_command_type__type="delivery")

    context = {"places": places, "locker": locker, "restaurant": restaurant}

    return render(request, "store/marketplaces.html", context)


@never_cache
def cart(request, info="show"):
    """if request method is GET : update cart value of the user depending of the
    stock and availability of varieties and load template to display his cart.

    if request method is POST : remove or update cart with data send by
    AJAX request
    """

    before(request)
    if request.method == "GET":
        if request.user.is_authenticated:
            client = Client.objects.get(user=request.user)
            update_cart_values(request, client)

            query = Cart.objects.filter(fk_client=client)

        else:
            # User is anonymous
            check_cart_session(request)
            cart_session = CartSession(request.session.get("cart"))
            cart_session.create_queryset(request)
            request.session["cart"] = cart_session.update(request)
            query = cart_session.return_queryset(request)

        total_cart = 0
        for product in query:
            product.total = product.quantity * product.fk_variety.price
            total_cart += product.total

        minimum = MinimumCommand.objects.all().first().amount

        if info == "outofstock":
            message = "Votre panier a été modifié en fonction \
            des stocks restants"
        elif info == "expire":
            message = "Votre session a expiré. Veuillez valider \
            à nouveau votre panier"
        else:
            message = ""

        context = {
            "cart": query,
            "total": total_cart,
            "minimum": minimum,
            "message": message,
        }

        return render(request, "store/cart.html", context)

    elif request.method == "POST":
        id_product = request.POST["cart_object"]

        if request.POST["action"] == "remove":

            if request.user.is_authenticated:
                client = Client.objects.get(user=request.user)
                variety_ref = Variety.objects.get(pk=id_product)

                cart_record = Cart.objects.get(
                    fk_client=client,
                    fk_variety=variety_ref
                )
                cart_record.delete()
            else:
                request.session["cart"].pop(id_product)
                request.session.modified = True

        elif request.POST["action"] == "update":
            quantity = request.POST["quantity"]
            stock = Variety.objects.get(pk=id_product).stock

            if request.user.is_authenticated:
                client = Client.objects.get(user=request.user)
                variety_ref = Variety.objects.get(pk=id_product)

                cart_record = Cart.objects.get(
                    fk_client=client,
                    fk_variety=variety_ref
                )

                if int(quantity) <= stock:
                    cart_record.quantity = quantity
                    cart_record.save()

            else:
                if int(quantity) <= stock:
                    request.session["cart"][id_product] = quantity
                    request.session.modified = True

        context = {}

        return JsonResponse(context)


def login_form(request):
    """Connect an existing user or create an account with data send by
    request POST ajax.
    """

    before(request)

    auth_email = request.POST["email"].lower()
    password = request.POST["password"]

    if request.POST["choice"] == "connect":
        try:
            u = User.objects.get(username=auth_email)
            if u.check_password(password):
                user = authenticate(username=auth_email, password=password)
                login(request, user)
                message = "success"

                client = Client.objects.get(user=user)

                check_cart_session(request)
                cart = CartSession(request.session.get("cart"))
                cart.create_queryset(request)
                cart.to_cart_database(request, client, add_to_cart)

            else:
                message = "incorect password"

        except User.DoesNotExist:
            message = "incorrect id"

    elif request.POST["choice"] == "create":
        name = request.POST["name"]

        try:
            u = User.objects.get(username=auth_email)
            message = "already exists"
        except User.DoesNotExist:
            u = User.objects.create_user(
                username=auth_email, password=password, first_name=name
            )

            number = request.POST["number"]
            street = request.POST["street"].lower()
            cplt = request.POST["cplt"].lower()
            cp = request.POST["cp"]
            city = request.POST["city"].lower()

            try:
                adress_form = Adress.objects.get(
                    numero=number,
                    rue=street,
                    complement=cplt,
                    code_postal=cp,
                    ville=city,
                )
            except Adress.DoesNotExist:
                adress_form = Adress.objects.create(
                    numero=number,
                    rue=street,
                    complement=cplt,
                    code_postal=cp,
                    ville=city,
                )

            client = Client.objects.create(
                user=u,
                phone=request.POST["phone"],
                fk_client_type=ClientType.objects.get(
                    type_client=request.POST["type"]),
                fk_adress=adress_form,
            )

            user = authenticate(username=auth_email, password=password)
            login(request, user)

            check_cart_session(request)
            cart = CartSession(request.session.get("cart"))
            cart.create_queryset(request)
            cart.to_cart_database(request, client, add_to_cart)

            message = "success"

    context = {"message": message}

    return JsonResponse(context)


def profil(request, info="show"):
    """If request method is GET : load template to display profil infos of
    the user. If request method is POST : update user or update password
    depending of action send by AJAX request
    """

    before(request)
    client = Client.objects.get(user=request.user)
    if request.method == "GET":

        order = Order.objects.filter(fk_client=client)

        actual_order = OrderHistoric.objects.filter(
            fk_order__in=order,
            date_end__isnull=True,
            date_cancellation__isnull=True
        )

        for elt in actual_order:
            ref_order = elt.fk_order
            elt.queryset_variety = OrderDetail.objects.filter(
                fk_order=ref_order
            )

        past_order = OrderHistoric.objects.filter(
            fk_order__in=order,
            date_end__isnull=False,
            date_cancellation__isnull=True
        )

        for elt in past_order:
            ref_order = elt.fk_order
            elt.queryset_variety = OrderDetail.objects.filter(
                fk_order=ref_order
            )

        if info == "success":
            message = "Votre commande a été enregistrée !"
        else:
            message = ""

        context = {
            "email": request.user.get_username(),
            "client": client,
            "actual_order": actual_order,
            "past_order": past_order,
            "message": message,
        }

        return render(request, "store/profil.html", context)

    elif request.method == "POST":
        if request.user.check_password(request.POST["password"]):
            if request.POST["action"] == "update_infos":
                request.user.username = request.POST["email"]
                request.user.first_name = request.POST["name"]

                number = request.POST["number"]
                street = request.POST["street"].lower()
                cplt = request.POST["cplt"].lower()
                cp = request.POST["cp"]
                city = request.POST["city"].lower()
                try:
                    adress_form = Adress.objects.get(
                        numero=number,
                        rue=street,
                        complement=cplt,
                        code_postal=cp,
                        ville=city,
                    )
                except Adress.DoesNotExist:
                    adress_form = Adress.objects.create(
                        numero=number,
                        rue=street,
                        complement=cplt,
                        code_postal=cp,
                        ville=city,
                    )

                client.fk_adress = adress_form

                client.phone = request.POST["phone"]

                client.save()
                request.user.save()
                message = "success"

            elif request.POST["action"] == "update_password":
                request.user.set_password(request.POST["newpassword"])
                request.user.save()
                update_session_auth_hash(request, request.user)

                message = "success"

        else:
            message = "incorrect_pass"

        context = {"message": message}

        return JsonResponse(context)


def logout_account(request):
    """ Disconect the authenticated user"""

    before(request)
    if request.user.is_authenticated:
        logout(request)
    return redirect("store:index")


def delete_account(request):
    """ Delete the user and all relatives datas from the database"""

    before(request)
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.get_username())
        logout(request)
        user.delete()

    return redirect("store:index")


def adding_in_cart(request):
    """Add product in cart of the user, in database if he's authenticated,
    or in the cart dictionry session if he's not
    """

    before(request)
    id_product = request.POST["product"]
    quantity = request.POST["quantity"]
    variety = Variety.objects.get(pk=id_product)

    if request.user.is_authenticated:
        client = Client.objects.get(user=request.user)
        add_to_cart(request, client, variety, quantity)
    else:
        # User is anonymous
        check_cart_session(request)
        request.session["cart"][id_product] = quantity
        request.session.modified = True

    context = {"message": "ok"}

    return JsonResponse(context)


def email(request):
    """ send an email to the admin farmer """

    before(request)
    admin_mail = User.objects.get(username="admin@farm").email

    email = EmailMessage(
        request.POST["subject"],
        request.POST["message"],
        request.POST["email"],
        [
            admin_mail,
        ],
    )

    try:
        email.send()
        message = "success"
    except Exception:
        message = "fail"

    context = {"message": message}
    return JsonResponse(context)


def reservation(request):
    """Try to reserve all items in cart's user from the variety stock.
    If stocks are not enough, url target is cart template, if they are,
    url target is a template for order, and client is adding in the
    ready to command list
    """

    button_cart = request.POST.get("button", False)
    if button_cart:
        client = Client.objects.get(user=request.user)
        cart = Cart.objects.filter(fk_client=client)

        try:
            with transaction.atomic():
                for obj in cart:
                    variety = obj.fk_variety
                    variety.stock = F("stock") - obj.quantity
                    variety.save()

        except IntegrityError:
            update_cart_values(request, client)

            url_cible = reverse("store:cart", kwargs={"info": "outofstock"})
        else:
            ClientReadyToCommand.objects.create(
                fk_client=client, validation_date=datetime.datetime.now()
            )
            url_cible = reverse("store:command")

        context = {
            "url": url_cible,
        }

        return JsonResponse(context)


@never_cache
def command(request):
    """ load the template to order the reserved cart"""

    if "Referer" in request.headers:
        client = Client.objects.get(user=request.user)
        cart = Cart.objects.filter(fk_client=client)
        cart_user = UserCart(client)
        total_cart, cart = cart_user.total()

        places = DirectWithdrawal.objects.all()
        restaurant = DeliverySlots.objects.all()

        locker_location = CollectLocation.objects.filter(
            fk_command_type__type="locker"
        )
        for location in locker_location:
            list = Locker.objects.filter(
                fk_collect_location=location.id, disponibility=True
            )
            if len(list) == 0:
                locker_location = locker_location.exclude(name=location.name)

        context = {
            "cart": cart,
            "total": total_cart,
            "directwithdrawal": places,
            "locker": locker_location,
            "delivery": restaurant,
            "client_type": client.fk_client_type.type_client,
        }

        return render(request, "store/command.html", context)

    else:
        return redirect("store:index")  # avoid access from adress bar


def validate_command(request):
    """If client is no longer in the ready list, redirect to the template
    cart. If he is, try to process to ordering reserved cart and, if succeed,
    redirect to profil template
    """

    cible = ""
    message = ""
    if request.method == "POST":  # good request origin
        client = Client.objects.get(user=request.user)
        cart = Cart.objects.filter(fk_client=client)
        client_in_list = ClientReadyToCommand.objects.filter(fk_client=client)

        if not client_in_list:
            update_cart_values(request, client)
            cible = reverse("store:cart", kwargs={"info": "expire"})
            context = {"url": cible, "response": "expire"}

            return JsonResponse(context)

        try:
            client_ready = ClientReadyToCommand.objects.get(fk_client=client)
            client_ready.block = True
            client_ready.save()

            with transaction.atomic():

                # !!!! PROCESS TO PAIEMENT !!!!

                choice = request.POST["choice"]
                if choice == "withdrawal":
                    option = request.POST["option_withdrawal"]
                    order = Order.objects.create(
                        fk_client=client,
                        fk_direct_withdrawal=DirectWithdrawal.objects.get(
                            pk=option
                        ),
                    )
                elif choice == "clickcollect":
                    option = request.POST["option_click"]
                    locker_location = CollectLocation.objects.get(pk=option)
                    locker_available = Locker.objects.filter(
                        fk_collect_location=locker_location, disponibility=True
                    )
                    assert len(locker_available) > 0

                    locker = locker_available.first()
                    locker.disponibility = False
                    locker.save()

                    order = Order.objects.create(
                        fk_client=client,
                        fk_locker=locker
                    )
                else:
                    instructions = request.POST["instructions"]
                    delivery = Delivery.objects.create(
                        instructions=instructions, fk_delivery_slot=choice
                    )

                    order = Order.objects.create(
                        fk_client=client,
                        fk_delivery=delivery
                    )

                # hstioric
                OrderHistoric.objects.create(fk_order=order)

                # order details
                for elt in cart:
                    OrderDetail.objects.create(
                        fk_order=order,
                        fk_variety=elt.fk_variety,
                        quantity=elt.quantity
                    )

                response = "success"
                cible = reverse("store:account", kwargs={"info": "success"})
                cart.delete()
                client_ready.delete()

        except AssertionError:
            response = "noLocker"
            message = "Désolé, il n'y a plus aucun casier disponible !"
            client_ready.block = False
            client_ready.save()

        except Exception:
            raise
            response = "Error"
            message = "Désolé, une erreur s'est produite"
            client_ready.block = False
            client_ready.save()

        context = {"url": cible, "message": message, "response": response}

        return JsonResponse(context)

    else:
        return redirect("store:index")


def remove_order(request):
    """Remove and order of th client and all relative informations
    from the database
    """

    if request.method == "POST":
        order_ref = request.POST["id"]
        order = Order.objects.get(pk=order_ref)
        response = ""
        with transaction.atomic():
            # !!!! PROCESS TO THE REFUND !!!!

            detail = OrderDetail.objects.filter(fk_order=order)
            for obj in detail:
                variety = obj.fk_variety
                variety.stock = F("stock") + obj.quantity
                variety.save()

            order.delete()

            response = "Commande supprimée"

        context = {
            "response": response,
        }
        return JsonResponse(context)

    else:
        return redirect("store:account")


def notfound(request, exception):
    """ load a custom 404 page of an error 404 occurs"""

    return render(request, "store/404.html", status=404)
