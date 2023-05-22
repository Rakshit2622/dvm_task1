from django.db import models
from vendors.models import VendorItems
from users.models import (
    CustomUser,
    VendorUser,
    CustomerUser,
    VendorProfile,
    CustomerProfile,
)
from django.utils import timezone
from django.urls import reverse


class Cart(models.Model):
    customer = models.OneToOneField(
        CustomerUser, on_delete=models.CASCADE, related_name="cart_customer"
    )
    bill_amt = models.PositiveIntegerField(default=0)

    def get_bill_amt(self):
        return sum([(x.total) for x in self.cart_end.all()])


class Cart_Items(models.Model):
    item = models.ForeignKey(
        VendorItems, on_delete=models.CASCADE, related_name="cart_item"
    )
    vendor = models.ForeignKey(
        VendorUser, on_delete=models.CASCADE, related_name="cart_items_vendor"
    )
    customer = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="cart_items_customer"
    )
    quantity = models.PositiveIntegerField(default=0)
    total = models.FloatField(null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_end")

    def get_absolute_url(self):
        return reverse("home", kwargs={"pk": self.pk})


class Order(models.Model):
    vendor = models.ForeignKey(
        VendorUser, on_delete=models.CASCADE, related_name="order_vendor"
    )
    customer = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="order_customer"
    )
    item_order = models.ForeignKey(
        VendorItems, on_delete=models.CASCADE, related_name="order_item"
    )
    quantity_order = models.PositiveIntegerField()
    total_order = models.FloatField()
    address = models.TextField()
    order_place = models.BooleanField(default=False)
    date_time_order = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    review = models.TextField()
    customer_review = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="review_customer"
    )
    item_review = models.ForeignKey(
        VendorItems, on_delete=models.CASCADE, related_name="item_review"
    )
    date_time_review = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    wishlist_item = models.ForeignKey(
        VendorItems, on_delete=models.CASCADE, related_name="wishlist_item"
    )
    customer = models.ForeignKey(
        CustomerUser, on_delete=models.CASCADE, related_name="wishlist_customer"
    )
