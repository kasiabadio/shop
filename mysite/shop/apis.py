from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from .models import *
from django.db import connection

# add item to cart
@api_view(["POST"])
def update_item(request):
    
    data = json.loads(json.dumps(request.data))
    product_id = int(float(data['product_id']))
    producent_id = int(float(data['producent_id']))
    
    if request.user.is_authenticated:
        current_user = request.user
        
        product = Produkt.objects.get(id_produktu=product_id)
        # create zamowienie: (id, id_zamowienie, czy_oplacone, sposob_dostawy, status, koszt, czat_id, reklamacja_id, klient_id, producent_id)
        zamowienie, created = Zamowienie.objects.get_or_create(czy_oplacone=False, status=60, koszt=0, klient_id=current_user.id_user, producent_id=producent_id)
        print("New order had to be created: ", created)
        
        # create zamowienieproduct: (id, quantity, produkt_id, zamowienie_id)
        print("producent_id", producent_id)
        print("produkt_id: ", product_id)
        print("zamowienie.id_zamowienie: ", zamowienie.id_zamowienie)
        
        zamowienieproduct, created = ZamowienieProdukt.objects.get_or_create(produkt_id=product_id, zamowienie_id=zamowienie.id)
        if not created:
            print("Increase quantity by one in ZamowienieProdukt")
            zamowienieproduct.quantity += 1
            zamowienieproduct.save()
        else:
            zamowienieproduct.quantity = 1
            zamowienieproduct.save()
            print("New ZamowienieProdukt had to be created")
            
        # increase koszt of zamowienie 
        zamowienie.koszt += product.cena
        zamowienie.save()

    return JsonResponse('Item was added to cart', safe=False)


@api_view(["POST"])
def add_product_to_database(request):

    if request.user.is_authenticated and request.user.is_producent:
        
        print('User is authenticated')
        current_user = request.user
        
        data = json.loads(json.dumps(request.data))
        
        nazwa = str(data['nazwa'])        
        numer_partii = int(float(data['numer_partii']))
        cena = float(data['cena'])
        opis = str(data['opis'])
        liczba = int(float(data['liczba']))
        image = str(data['image'])
        is_hidden_TF = str(data['is_hidden'])
        is_hidden = 1
        if is_hidden_TF == 'Nie': is_hidden = 0
        
        producent_id = request.user.id_user
        
        kategoria_nazwa = str(data['kategoria'])
        print(kategoria_nazwa)
        kategoriaa = Kategoria.objects.get(nazwa_kategorii=kategoria_nazwa)
        
        # dodaj produkt
        product = Produkt.objects.create(nazwa=nazwa, numer_partii=numer_partii,
                                         cena=cena, opis=opis, liczba=liczba, image=image,
                                         producent_id=producent_id, is_hidden=is_hidden)
        
        # dodaj produkt - kategoria
        cursor = connection.cursor()
        query = """INSERT INTO shop_produkt_kategoria
        (id, produkt_id, kategoria_id)
        VALUES((SELECT MAX(id) FROM shop_produkt_kategoria)+1,""" + str(product.id_produktu) + "," + str(kategoriaa.id_kategorii) + ");"
        cursor.execute(query)
        
    else:
        print('User is not defined')
    
    return JsonResponse('Item was added to database', safe=False)


@api_view(["POST"])
def edit_product(request):
    data = json.loads(json.dumps(request.data))
    new_opis = data['opis']
    product = Produkt.objects.get(id_produktu=int(data['product_id']))
    product.opis = new_opis
    product.save()
    return JsonResponse('Product was deleted', safe=False)


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


# remove order from cart
@api_view(["POST"])
def remove_order(request):
    
    data = json.loads(json.dumps(request.data))
    print("remove (order_id): " + data['order_id'])
    record = Zamowienie.objects.get(id=int(data['order_id']))
    record.delete()
    
    # remove all related products to order from cart
    related_products = ZamowienieProdukt.objects.get(zamowienie_id=int(data['order_id']))
    related_products.delete()
    
    return JsonResponse('Order was deleted from cart', safe=False)


# remove product from order in cart
@api_view(["POST"])
def remove_product(request):
    
    data = json.loads(json.dumps(request.data))
    print("remove (order_id, product_id): " + data['order_id'] + " " + data['product_id'])
    
    # remove zamowienie - produkt
    record = ZamowienieProdukt.objects.get(produkt_id=int(data['product_id']), zamowienie_id=int(data['order_id']))
    record.delete()
    
    # if this was the last product, remove order
    cursor = connection.cursor()
    query = """SELECT COUNT(*) FROM shop_zamowienieprodukt
    WHERE zamowienie_id=""" + data['order_id'] + ";"
    cursor.execute(query)
    counter = cursor.fetchall()
    cursor.close()
    
    if counter[0][0] == 0: 
        record = Zamowienie.objects.get(id=int(data['order_id']))
        record.delete()

    return JsonResponse('Product was deleted from order in cart', safe=False)


# confirm order in checkout
@api_view(["POST"])
def process_order(request):
    
    data = json.loads(json.dumps(request.data))
    order_number = int(float(data['order_number']))
    print('Order number: ', order_number, type(order_number))
    
    # change status from 1 (in checkout) to 2 (made payment)
    # note: here could implement payment method
    order = Zamowienie.objects.get(id=order_number)
    order.status = 2
    order.czy_oplacone = True
    order.save()
    
    return JsonResponse('Order in checkout was payed', safe=False)
