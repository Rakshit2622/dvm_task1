from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, VendorProfile, VendorUser, CustomerUser, CustomerProfile
from orders.models import Cart


@receiver(post_save, sender=VendorUser, weak=False)
def create_vendor_profile(sender, instance, created, **kwargs):
    if created:
        VendorProfile.objects.create(vendor_user_profile=instance)


@receiver(post_save, sender=CustomerUser, weak=False)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(customer_user_profile=instance)
        Cart.objects.create(customer=instance)
