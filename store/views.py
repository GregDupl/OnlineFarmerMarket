from django.shortcuts import render
from store.models import *
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
    return render(request,'store/marketplaces.html')

def cart(request):
    return render(request,'store/cart.html')
