from django.urls import path
from . import views as order_views

urlpatterns = [
	path('add/<int:pk>',order_views.add_to_cart,name='add_to_cart'),
	path('cart/',order_views.cart_list,name='cart_list'),
	path('cart/delete/',order_views.remove_from_cart,name='remove_from_cart'),
	path('cart/order/',order_views.order,name='order')
]