from django.urls import path, include

from . import views

app_name = "store"

urlpatterns = [
    path('', views.index, name="index"),
    path('marcheenligne', views.webmarket, name="webmarket"),
    path('pointsdevente', views.marketplaces, name="marketplaces"),
    path('panier', views.cart, name="cart"),
    path('login', views.login_form, name="login"),
    path('account', views.profil, name="account"),
    path('logout', views.logout_account, name="logout"),
    path('delete', views.delete_account, name="delete_account"),
    path('cart', views.adding_in_cart, name="adding_cart"),
    path('remove', views.remove, name="remove"),
]
