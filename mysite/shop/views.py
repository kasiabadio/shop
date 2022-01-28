from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from .models import *
from django.db import connection
from django.template.defaulttags import register
from rest_framework.decorators import api_view
import json
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from .forms import SignUpForm
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def login_view(request):
    
    if request.user.is_authenticated:
        
        print("Already logged in")
        return redirect('shop')
        
    elif request.method == 'POST':
        
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
                
            user = form.get_user()
            if user is not None:
           
                auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print("Logged in")
                return redirect('shop')
                
    else:
        form = AuthenticationForm()
        
    return render(request, 'shop/login.html', {'form': form })
    
    
def signup(request):
    
    if request.user.is_authenticated:
        
        print("Logged in - can not register")
        return redirect('shop')
    
    elif request.method == 'POST':
        
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            
            # create client or producent accordingly to fields is_producent and is_klient
            if user.is_klient == True: 
                klient, created = Klient.objects.get_or_create(id_klienta=user)
                print("New klient was created: ", created)
                
            elif user.is_producent == True:
                producent, created = Producent.objects.get_or_create(id_producenta=user)
                print("New producent was created: ", created)
      
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print('Signup successfull')
            return redirect('shop')
    else:
        form = SignUpForm()
        
    return render(request, 'shop/signup.html', {'form': form })
        
        
        
def logout_view(request):
    
    if request.user.is_authenticated:
        logout(request)
        print('Logout successfull')
        
    return redirect('shop')


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

    return JsonResponse('Item was added to cart', safe=False)


# Main page for shop: search (products/)
# access: CLIENT, PRODUCENT
def shop(request):
    
    products = Produkt.objects.all()
    super_categories = Kategoria.objects.all().filter(id_nadkategorii=None)
    
    # create dictionary where we store subcategories     
    super_categories_dict = {}
        
    for category in super_categories:
        
        sub_categories = Kategoria.objects.all().filter(id_nadkategorii=category.id_kategorii)
        super_categories_dict[category] = sub_categories
            
    context = {'products': products, 'super_categories_dict': super_categories_dict}
    return render(request, 'shop/main.html', context)


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
        producent_id = request.user.id_user
        
        kategoria_nazwa = str(data['kategoria'])
        print(kategoria_nazwa)
        kategoriaa = Kategoria.objects.get(nazwa_kategorii=kategoria_nazwa)
        
        # dodaj produkt
        product = Produkt.objects.create(nazwa=nazwa, numer_partii=numer_partii,
                                         cena=cena, opis=opis, liczba=liczba, image=image,
                                         producent_id=producent_id)
        
        # dodaj produkt - kategoria
        cursor = connection.cursor()
        query = """INSERT INTO shop_produkt_kategoria
        (id, produkt_id, kategoria_id)
        VALUES((SELECT MAX(id) FROM shop_produkt_kategoria)+1,""" + str(product.id_produktu) + "," + str(kategoriaa.id_kategorii) + ");"
        cursor.execute(query)
        
    else:
        print('User is not defined')
    
    return JsonResponse('Item was added to database', safe=False)


# Page for adding product to a database, modifying visibility for existing products
# access: PRODUCENT
def manage(request):
    
    products = {}
    pc = {}
    current_user = 'Anonymous'
    subcategories = {}
    
    if request.user.is_authenticated:
        
        print('User is authenticated')
        print(request.user.username)
        current_user = request.user.username
        
        if request.user.is_klient:
            print('Jest klientem: ', request.user.is_klient)
            return redirect('shop')
    
        try:
            print('Jest producentem: ', request.user.is_producent)
            
            # wybierz produkty należące tylko do tego producenta
            products = Produkt.objects.all().filter(producent_id=request.user.id_user)
            product_categories = Produkt.kategoria.through.objects.all()
            
            # przejdź po id produktu, dodaj do słownika id kategorii i nazwę
            for prodcat in product_categories:
                if prodcat.produkt_id not in pc:
                    pc[prodcat.produkt_id] = str(Kategoria.objects.all().filter(id_kategorii=prodcat.kategoria_id))[23:-3]
                    # print(prodcat.produkt_id, pc[prodcat.produkt_id], type(pc[prodcat.produkt_id]))
                                       
            # create dictionary where we store subcategories     
            subcategories = Kategoria.objects.all().filter(~Q(id_nadkategorii=None))
            
            context = {'current_user': current_user, 'products': products , 'pc': pc , 
               'subcategories': subcategories }
            
            return render(request, 'shop/manage.html', context)
                                    
        except User.producent.RelatedObjectDoesNotExist:   
            print ("User is not defined")
    
    
    return redirect('shop')
    

# Page for viewing orders
# access: PRODUCENT, CLIENT
def orders(request):
    
    orders = {}
    current_user = 'Anonymous'
    if request.user.is_authenticated:
        
        print('User is authenticated')
        print(request.user.username)
        current_user = request.user
        
        # Wybierz wszystkie zamówienia klienta
        if request.user.is_klient:
            print("Selecting client's orders")
            orders = Zamowienie.objects.all().filter(klient_id=current_user.id_user)
              
        # Wybierz wszystkie zamówienia producenta
        elif request.user.is_producent:
            print("Selecting producent's orders")
            orders = Zamowienie.objects.all().filter(producent_id=current_user.id_user)
            
    context = {'current_user': current_user, 'orders': orders }
    return render(request, 'shop/orders.html', context)
                                    
    

# TODO: fix
# Displays info about category
# access: CLIENT, PRODUCENT
class Category(DetailView):
    model = Kategoria
    template_name = 'shop/category.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        cursor = connection.cursor()
        query = """SELECT produkt_id FROM shop_produkt_kategoria
        WHERE kategoria_id=""" + str(self.object.id_kategorii) + ";"
        cursor.execute(query)
        context['product_categorias'] = cursor.fetchall()
        cursor.close()
        
        products = []
        for product_cat in context['product_categorias']:
            product_cat_parsed = int(float(product_cat[0]))
            product_in_category = Produkt.objects.get(id_produktu=product_cat_parsed)
            products.append(product_in_category)
            print(products)
            
        print(products[0].nazwa)
        context['products'] = products
        return context


# Displays info about product
# access: CLIENT, PRODUCENT
class Product(DetailView):
    model = Produkt
    template_name = 'shop/product.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


# Page where user can see his order which contains orders from specific producents
# access: CLIENT

def cart(request):
    
    orders_for_user = {}
    current_user = 'Anonymous'
    cart_products = {}
    cart_sum = {}
    shipping_type = 0
    cart_producents = []
    all = {}
    

    if request.user.is_authenticated:
        
        print('User is authenticated')
        print(request.user.username)
        
        if request.user.is_producent:
            return redirect('shop')
        
        try:
            
            current_user = request.user.klient
            # filter elements by current user id and display only his order & select only those orders which were not paid
            orders_for_user = Zamowienie.objects.all().filter(status=60).filter(klient=current_user).filter(czy_oplacone=False)
            
            # get all products for each order & get producents from all orders 
            all = ZamowienieProdukt.objects.all()
            
            for order in orders_for_user:
                print("ORDER ID: ", order.id)
                cart_producents.append(order.producent_id)
                
                # get all products id's in an order
                orderproducts = ZamowienieProdukt.objects.all().filter(zamowienie_id=order.id)

                # get all products info from products table having orderproducts info
                orderproducts_all = []
                order_sum = 0
                for zamowienieproduct in orderproducts:
                    product = Produkt.objects.get(id_produktu=zamowienieproduct.produkt_id)
                    print(product.id_produktu)
                    orderproducts_all.append(product)
                    order_sum += zamowienieproduct.get_total
                    
                # add all products to cart_products dictionary
                if order.id not in cart_products:
                    cart_products[order.id] = orderproducts_all
                
                # add cart sum to cart_sum dictionary
                if order.id not in cart_sum:
                    cart_sum[order.id] = order_sum
                    
            shipping_type = Zamowienie.sposob_dostawy
            
            
        except User.klient.RelatedObjectDoesNotExist:
            
            print ("User is not defined")
    
    print(cart_products)
    context = {'orders_for_user': orders_for_user, 'current_user': current_user, 
               'cart_products': cart_products, 'cart_sum': cart_sum, 'shipping_type': shipping_type, 
               'cart_producents': cart_producents, 'all': all}
    
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



# Page where user can finalize order 
# access: CLIENT
def checkout(request):
    
    order = {}
    order_sum = 0
    orderproducts = {}
    orderproducts_all = []
    current_user = "Anonymous"
    
    if request.user.is_producent:
            return redirect('shop')

    if request.user.is_authenticated:
        
        print ("User is authenticated")
        print(request.user.username)
        
        try:
            
            current_user = request.user.klient
            
            # filter elements by current user id and display only his order which he selected in cart
            order = Zamowienie.objects.all().filter(klient=current_user).filter(status=1)
                
            # get all products info from products table having orderproducts info
            for ord in order:
                orderproducts = ZamowienieProdukt.objects.all().filter(zamowienie_id=ord.id_zamowienie)
                break
            
            for zamowienieproduct in orderproducts:
                product = Produkt.objects.get(id_produktu=zamowienieproduct.produkt_id)
                orderproducts_all.append(product)
                order_sum += zamowienieproduct.get_total
                
                
        except User.klient.RelatedObjectDoesNotExist:
            
            print ("User is not defined")
    
    else:
        print("User is not authenticated")
       
       
    context = {'order': order, 'order_sum': order_sum, 'orderproducts': orderproducts,
                'orderproducts_all': orderproducts_all, 'current_user': current_user} 
        
    return render(request, 'shop/checkout.html', context)
    

# Page where client or producent can see his messages and write a new one
# access: CLIENT, PRODUCENT
def messages(request):
    context = {}
    return render(request, 'shop/messages.html')