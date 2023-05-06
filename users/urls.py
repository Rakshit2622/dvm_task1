from django.urls import path
from users import views as users_views

urlpatterns=[
	path('register/vendor-registration/',users_views.vendor_register,name='vendor-register-view'),
	path('register/customer-registration/',users_views.customer_register,name='customer-register-view'),
	path('register/',users_views.register_view,name='register'),
	path('vendor-profile/',users_views.vendor_profile,name='vendor-profile'),
	path('customer-profile/',users_views.customer_profile,name='customer-profile'),
	path('login-redirect/',users_views.login_redirect,name='login-redirect'),
	path('add-money/',users_views.add_money,name='add-money'),
]