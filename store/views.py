from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'store/index.html')

def webmarket(request):
    context = {
    "product" : [
        { "nom" : "aubergines", "prix" : "2", "unité" : "kg", "Category" : "Légumes"},
        { "nom" : "tomates", "prix" : "2", "unité" : "kg", "Category" : "Légumes"},
        { "nom" : "carottes", "prix" : "1", "unité" : "bottes", "Category" : "Légumes"},
        { "nom" : "comté", "prix" : "10", "unité" : "kg", "Category" : "Fromages"},
        { "nom" : "pommes", "prix" : "2", "unité" : "kg", "Category" : "Fruits"}
    ],
    "category" : [
    {"name" : "Légumes"},
    {"name" : "Fruits"},
    {"name" : "Miel"},
    {"name" : "Fromages"},
    {"name" : "Oeufs"},
    ]
    }
    return render(request,'store/webmarket.html', context)
