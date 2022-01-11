from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db import connection
from .models import *
from django.db import connection
from django.template.defaulttags import register
from rest_framework.decorators import api_view
import json
from django.core.exceptions import ObjectDoesNotExist


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# # Calculate sum of all orders of a user
# def calculate_sum_koszyk(klient):
#     with connection.cursor() as cursor:
#         sum_koszyk = cursor.callproc('calculate_sum_koszyk', [klient])
#     return sum_koszyk

# Calculate sum of a single order (sql1.py)
# def calculate_sum_zamowienie(zamowienie):
#     with connection.cursor() as cursor:
#         sum_zamowienie = cursor.callproc('calculate_sum_zamowienie', [zamowienie])
#     return sum_zamowienie
#-----------------------------------------------

# add item to cart
@api_view(["POST"])
def update_item(request):
    
    data = json.loads(json.dumps(request.data))
    product_id = int(float(data['product_id']))
    producent_id = int(float(data['producent_id']))
    current_user = 1
    
    product = Produkt.objects.get(id_produktu=product_id)
    # create zamowienie: (id, id_zamowienie, czy_oplacone, sposob_dostawy, status, koszt, czat_id, reklamacja_id, klient_id, producent_id)
    zamowienie, created = Zamowienie.objects.get_or_create(czy_oplacone=False, status=60, koszt=0, klient_id=1, producent_id=producent_id)
    print("New order had to be created: ", created)
 
    
    # create zamowienieproduct: (id, quantity, produkt_id, zamowienie_id)
    print("producent_id", producent_id)
    print("produkt_id: ", product_id)
    print("zamowienie.id_zamowienie: ", zamowienie.id_zamowienie)
    
    
    try:
        # user wants to increase quantity of a product
        zamowienieprodukt = ZamowienieProdukt.objects.get(produkt_id=product_id, zamowienie_id=zamowienie.id_zamowienie)
        zamowienieprodukt.quantity += 1
        zamowienieprodukt.save()
        print("Increase quantity by one in ZamowienieProdukt")
        
    except ObjectDoesNotExist:
        # user added new product to a cart
        ZamowienieProdukt.objects.create(quantity=1, produkt_id=product_id, zamowienie_id=zamowienie.id_zamowienie)
        print("New ZamowienieProdukt had to be created")
        
    
    return JsonResponse('Item was added to cart', safe=False)



# Main page for shop: search (products/)
# access: CLIENT, PRODUCENT
def shop(request):
    
    products = Produkt.objects.all()
    context = {'products': products}
    
    # TODO: categories 
            
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
    
    products = Produkt.objects.all()
    context = {'products': products}
    
    return render(request, 'shop/category.html', context)


# Displays info about product
# access: CLIENT, PRODUCENT
def product(request):
    context = {}
    return render(request, 'shop/product.html')


# Page where user can see his order which contains orders from specific producents
# access: CLIENT
def cart(request):
    
    # if request.user.is_authenticated:
        
    # klient = request.user.klient
        
        # filter elements by current user id and display only his order
        #orders_for_user = Zamowienie.objects.get_or_create(klient=klient)
        
    # select only those orders which were not paid
    orders_for_user = Zamowienie.objects.all().filter(status=60).filter(klient=1).filter(czy_oplacone=False)
    current_user = 1
    
    # calculate sum of a cart
    cart_total = 0
    
    # get all products for each order
    # get producents from all orders 
    cart_products = {}
    cart_sum = {}
    products_sum = {}
    cart_producents = []
    all = ZamowienieProdukt.objects.all()
    for order in orders_for_user:
        cart_producents.append(order.producent_id)
        
        # get all products id's in an order
        orderproducts = ZamowienieProdukt.objects.all().filter(zamowienie_id=order.id_zamowienie)

        # get all products info from products table having orderproducts info
        orderproducts_all = []
        order_sum = 0
        for zamowienieproduct in orderproducts:
            product = Produkt.objects.get(id_produktu=zamowienieproduct.produkt_id)
            orderproducts_all.append(product)
            order_sum += zamowienieproduct.get_total
            
        cart_total += order_sum
        
        # add all products to cart_products dictionary
        if order.id_zamowienie not in cart_products:
            cart_products[order.id_zamowienie] = orderproducts_all
        
        # add cart sum to cart_sum dictionary
        if order.id_zamowienie not in cart_sum:
            cart_sum[order.id_zamowienie] = order_sum
            
    shipping_type = Zamowienie.sposob_dostawy
        
    # else:
    #     orders_for_user = []
    #     current_user = -1
    #     cart_total = -1
    #     cart_products = []
    #     cart_sum = []
    #     shipping_type = 0
    #     cart_producents = []
    #     all = []
    
    
    context = {'orders_for_user': orders_for_user, 'current_user': current_user, 'cart_total': cart_total, 
               'cart_products': cart_products, 'cart_sum': cart_sum, 'shipping_type': shipping_type, 
               'cart_producents': cart_producents, 'orderproducts_all': all}
    
    return render(request, 'shop/cart.html', context)


# choose which order is in checkout
@api_view(["POST"])
def curr_order_number(request):
    
    data = json.loads(json.dumps(request.data))
    order_number = int(float(data['order_number']))
    print('Order number: ', order_number, type(order_number))
    
    # change status from 60 (in cart) to 1 (in checkout)
    order = Zamowienie.objects.get(id=order_number)
    order.status = 1
    order.save()
    
    return JsonResponse('Order number was saved', safe=False)


# Page where user can finalize order 
# access: CLIENT
def checkout(request):
    
    # filter elements by current user id and display only his order which he selected in cart
    order = Zamowienie.objects.all().filter(klient=1).filter(status=1)
    current_user = 1
        
    # get all products info from products table having orderproducts info
    for ord in order:
        orderproducts = ZamowienieProdukt.objects.all().filter(zamowienie_id=ord.id_zamowienie)
        break
    
    orderproducts_all = []
    order_sum = 0
    for zamowienieproduct in orderproducts:
        product = Produkt.objects.get(id_produktu=zamowienieproduct.produkt_id)
        orderproducts_all.append(product)
        order_sum += zamowienieproduct.get_total
        
    
    context = {'order': order, 'order_sum': order_sum, 'orderproducts': orderproducts,
               'orderproducts_all': orderproducts_all, 'current_user': current_user}
    
    return render(request, 'shop/checkout.html', context)
    

# Page where client or producent can see his messages and write a new one
# access: CLIENT, PRODUCENT
def messages(request):
    context = {}
    return render(request, 'shop/messages.html')