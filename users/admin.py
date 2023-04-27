from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser ,VendorUser, CustomerUser ,VendorProfile ,CustomerProfile




admin.site.register(CustomUser)

admin.site.register(VendorUser)

admin.site.register(CustomerUser)

admin.site.register(VendorProfile)

admin.site.register(CustomerProfile)

