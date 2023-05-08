from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver 
from .models import VendorProfile , CustomUser, VendorUser,CustomerUser,CustomerProfile
from orders.models import Cart

@receiver(post_save,sender=VendorUser)
def create_profile(sender , instance ,created,**kwargs):
	if created:
		VendorProfile.objects.create(vendor_user_profile=instance)

@receiver(post_save,sender=CustomerUser)
def create_profile(sender , instance ,created,**kwargs):
	if created:
		CustomerProfile.objects.create(customer_user_profile=instance)
		Cart.objects.create(customer=instance)







