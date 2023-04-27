from django import forms 
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, VendorUser,CustomerUser,VendorProfile


class VendorRegisterForm(UserCreationForm):
	email=forms.EmailField()
	class Meta:
		model = VendorUser
		fields = ['email','password1','password2']



class CustomerRegisterForm(UserCreationForm):
	email=forms.EmailField()
	class Meta:
		model = CustomerUser
		fields = ['email','password1','password2']

	