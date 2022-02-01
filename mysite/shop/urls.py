from django.urls import path

from . import views
from .views import Category, Product

urlpatterns = [
    path('', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('category/<int:pk>/', Category.as_view(), name='Category'),
    path('checkout/', views.checkout, name='checkout'),
    path('manage/', views.manage, name='manage'),
    path('add_product_to_database/', views.add_product_to_database, name='add_product_to_database'),
    path('messages/', views.messages, name='messages'),
    path('orders/', views.orders, name='orders'),
    path('product/<int:pk>/', Product.as_view(), name='Product'),
    path('curr_order_number/', views.curr_order_number, name='curr_order_number'),
    path('update_item/', views.update_item, name='update_item'),
    path('remove_product/', views.remove_product, name='remove_product'),
    path('remove_order/', views.remove_order, name='remove_order'),
    path('process_order/', views.process_order, name='process_order'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
]

