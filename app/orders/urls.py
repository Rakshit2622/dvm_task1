from django.urls import path
from . import views as order_views
from .views import (
    OrderDetailView,
    ReviewCreateView,
    CartItemDeleteView,
    WishlistDeleteView,
)

urlpatterns = [
    path("add/<int:pk>", order_views.add_to_cart, name="add_to_cart"),
    path("cart/", order_views.cart_list, name="cart_list"),
    path("cart/<int:pk>/delete", CartItemDeleteView.as_view(), name="cart_item_delete"),
    path("cart/delete/", order_views.remove_from_cart, name="remove_cart"),
    path("cart/order/", order_views.order, name="order"),
    path("previous-orders/", order_views.order_customer_view, name="previous_orders"),
    path("vendor-orders/", order_views.order_vendor_view, name="vendor_orders"),
    path("order/<int:pk>/detail", OrderDetailView.as_view(), name="order-detail"),
    path(
        "order/<int:pk>/write-review",
        order_views.ReviewCreateView,
        name="create-review",
    ),
    path("wishlist/add/<int:pk>", order_views.add_to_wishlist, name="add_to_wishlist"),
    path(
        "wishlist/add-to-cart/<int:pk>", order_views.move_to_cart, name="move_to_cart"
    ),
    path("wishlist/", order_views.wishlist_list, name="wishlist_list"),
    path(
        "wishlist/delete/<int:pk>",
        WishlistDeleteView.as_view(),
        name="wishlist_item_delete",
    ),
    path("wishlist/delete", order_views.remove_wishlist, name="wishlist_delete"),
]
