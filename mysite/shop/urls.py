from django.urls import path

from . import views
from .views import Category, Product

urlpatterns = [
    path('', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('category/<int:pk>/', Category.as_view(), name='Category'),
    path('checkout/', views.checkout, name='checkout'),
    path('manage/', views.manage, name='manage'),
    path('messages/', views.messages, name='messages'),
    path('orders/', views.orders, name='orders'),
    path('product/<int:pk>/', Product.as_view(), name='Product'),
    path('curr_order_number/', views.curr_order_number, name='curr_order_number'),
    path('update_item/', views.update_item, name='update_item'),
    path('process_order/', views.process_order, name='process_order'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]