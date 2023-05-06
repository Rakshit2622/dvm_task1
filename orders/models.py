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
	item = models.ForeignKey(VendorItems,on_delete=models.CASCADE,related_name='cart_item')
	vendor = models.ForeignKey(VendorUser,on_ delete=models.CASCADE,related_name='cart_vendor')
	customer = models.ForeignKey(CustomerUser,on_delete=models.CASCADE,related_name='cart_customer')
	quantity = models.PositiveIntegerField()
	total = models.PositiveIntegerField()
	empty = models.BooleanField(default=False)




