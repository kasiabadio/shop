from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import *

# Main page for shop: search (products/)
# access: CLIENT, PRODUCENT
def shop(request):
    
    products = Produkt.objects.all()
    context = {'products': products}
    return render(request, 'shop/main.html', context)


# Page for adding product to a database, modifying visibility for existing products
# access: PRODUCENT
def manage(request):
    context = {}
    return render(request, 'shop/manage.html')


# Page for viewing orders
# access: CLIENT, PRODUCENT
def orders(request):
    context = {}
    return render(request, 'shop/orders.html')


# Displays info about category
# access: CLIENT, PRODUCENT
def category(request):
    context = {}
    return render(request, 'shop/category.html')


# Displays info about product
# access: CLIENT, PRODUCENT
def product(request):
    context = {}
    return render(request, 'shop/product.html')


# Page where user can see his order which contains orders from specific producents
# access: CLIENT
def cart(request):
    
    orders_for_user = Zamowienie.objects.all().filter(klient=1)
    current_user = 1
    context = {'orders_for_user': orders_for_user, 'current_user': current_user}
    return render(request, 'shop/cart.html', context)


# Page where user can finalize order 
# access: CLIENT
def checkout(request):
    
    orders = Zamowienie.objects.all()
    context = {'orders': orders}
    return render(request, 'shop/checkout.html', context)


# Page where client or producent can see his messages and write a new one
# access: CLIENT, PRODUCENT
def messages(request):
    context = {}
    return render(request, 'shop/messages.html')