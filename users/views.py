from django.shortcuts import render ,redirect
from .models import CustomUser,VendorUser,CustomerUser,VendorProfile
from django.contrib import messages
from .forms import VendorRegisterForm , CustomerRegisterForm 
from django.contrib.auth import login , authenticate 

def vendor_register(request):
	if request.method == 'POST':
		form = VendorRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			messages.success(request , f'Your account has been created!')
			return redirect('login')
	else:
		form = VendorRegisterForm()

	return render(request,'users/register_vendor.html',{'form':form})


def customer_register(request):
	if request.method == 'POST':
		form = CustomerRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			messages.success(request , f'Your account has been created!')
			return redirect('login')
	else:
		form = CustomerRegisterForm()

	return render(request,'users/register_customer.html',{'form':form})

def register_view(request):
	return render(request,'users/choose.html')

def vendor_profile(request):
	
	return render(request,'users/vendor_profile.html')

	
