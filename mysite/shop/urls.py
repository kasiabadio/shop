from django.urls import path

from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('category/', views.category, name='category'),
    path('checkout/', views.checkout, name='checkout'),
    path('manage/', views.manage, name='manage'),
    path('messages/', views.messages, name='messages'),
    path('orders/', views.orders, name='orders'),
    path('product/', views.product, name='product'),
    path('update_item/', views.update_item, name='update_item'),
]