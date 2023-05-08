from django import forms 
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, VendorUser, CustomerUser, VendorProfile , CustomerProfile


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

class VendorUpdateForm(forms.ModelForm):
	class Meta:
		model = VendorProfile
		fields = ['vendor_name','vendor_phone_no']

class CustomerUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomerProfile
		fields = ['customer_name','customer_address']

class CustomerImageForm(forms.ModelForm):
	class Meta:
		model = CustomerProfile
		fields = ['customer_image']

class CustomerMoneyForm(forms.ModelForm):
	class Meta:
		model = CustomerProfile
		fields = ['customer_money']
	

	