from django.urls import path
from users import views as users_views

urlpatterns=[
	path('register/vendor-registeration/',users_views.vendor_register,name='vendor-register-view'),
	path('register/customer-registeration/',users_views.customer_register,name='customer-register-view'),
	path('register/',users_views.register_view,name='register'),
	path('vendor-profile/',users_views.vendor_profile,name='vendor-profile'),
]