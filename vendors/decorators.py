from django.contrib import messages
from users.models import CustomUser 
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def customer_only(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(
        lambda u: u.is_customer and u.is_active,
        login_url='login',
        redirect_field_name=redirect_field_name
        )
    if function:
        return actual_decorator(function)
    return actual_decorator

def vendor_only(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    actual_decorator = user_passes_test(
        lambda u: u.is_vendor and u.is_active,
        login_url='login',
        redirect_field_name=redirect_field_name
        )
    if function:
        return actual_decorator(function)   
    return actual_decorator


