from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from .models import *
from django.db import connection
from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

# # Calulate sum of all orders of a user
# def calculate_sum_koszyk(klient):
#     with connection.cursor() as cursor:
#         sum_koszyk = cursor.callproc('calculate_sum_koszyk', [klient])
#     return sum_koszyk

# Calculate sum of a single order (sql1.py)
# def calculate_sum_zamowienie(zamowienie):
#     with connection.cursor() as cursor:
#         sum_zamowienie = cursor.callproc('calculate_sum_zamowienie', [zamowienie])
#     return sum_zamowienie

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
    
    
    # TODO: filter elements by current user id and display only his order
    orders_for_user = Zamowienie.objects.all().filter(klient=1)
    current_user = 1
    
    # calculate sum of a cart
    cart_sum = 0
    for order in orders_for_user:
        cart_sum += order.get_zamowienie_total
        
    # get all products for each order
    cart_products = {}
    for order in orders_for_user:
        products = Produkt.objects.all().filter(zamowienie_id=order.id_zamowienie)
        if order.id_zamowienie not in cart_products:
            cart_products[order.id_zamowienie] = products
            
    shipping_type = Zamowienie.sposob_dostawy
    
    context = {'orders_for_user': orders_for_user, 'current_user': current_user, 'cart_sum': cart_sum, 
               'cart_products': cart_products, 'shipping_type': shipping_type}
    return render(request, 'shop/cart.html', context)


# Page where user can finalize order 
# access: CLIENT
def checkout(request):
    
    # TODO: filter elements by current user id and display only his order (same as in cart)
    orders_for_user = Zamowienie.objects.all().filter(klient=1)
    current_user = 1
    
    # TODO: calculate sum of a cart
    
    orders = Zamowienie.objects.all()
    context = {'orders': orders, 'orders_for_user': orders_for_user, 'current_user': current_user}
    return render(request, 'shop/checkout.html', context)


# Page where client or producent can see his messages and write a new one
# access: CLIENT, PRODUCENT
def messages(request):
    context = {}
    return render(request, 'shop/messages.html')