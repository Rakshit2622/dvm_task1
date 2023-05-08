from django.db import models
from vendors.models import VendorItems
from users.models import (
	CustomUser,
	VendorUser,
	CustomerUser,
	VendorProfile,
	CustomerProfile
	)

class Cart(models.Model):
	item = models.OneToOneField(VendorItems,on_delete=models.CASCADE,related_name='cart_item',null=True,blank=True)
	vendor = models.OneToOneField(VendorUser,on_delete=models.CASCADE,related_name='cart_vendor',null=True,blank=True)
	customer = models.OneToOneField(CustomerUser,on_delete=models.CASCADE,related_name='cart_customer')
	quantity = models.PositiveIntegerField(default=0)
	total = models.FloatField(null=True,blank=True)
	full = models.BooleanField(default=False)

class Order(models.Model):
	vendor = models.ForeignKey(VendorUser,on_delete=models.CASCADE,related_name='order_vendor')
	customer = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name='order_customer')
	item_order =  models.ForeignKey(VendorItems,on_delete=models.CASCADE,related_name='order_item')
	quantity_order = models.PositiveIntegerField()
	total_order = models.FloatField()
	address = models.TextField()
	order_place = models.BooleanField(default=False)




