from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection


# Main page for shop: search (products/)
# access: CLIENT, PRODUCENT
def shop(request):
    context = {}
    return render(request, 'shop/main.html')


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
    context = {}
    return render(request, 'shop/cart.html')


# Page where user can finalize order 
# access: CLIENT
def checkout(request):
    context = {}
    return render(request, 'shop/checkout.html')


# Page where client or producent can see his messages and write a new one
# access: CLIENT, PRODUCENT
def messages(request):
    context = {}
    return render(request, 'shop/messages.html')