from django.shortcuts import render ,redirect
from .models import CustomUser,VendorUser,CustomerUser,VendorProfile , CustomerProfile
from django.contrib import messages
from .forms import (
	VendorRegisterForm,
	CustomerRegisterForm,
	VendorUpdateForm,
	CustomerUpdateForm,
	CustomerImageForm,
	CustomerMoneyForm,
	)
from django.contrib.auth import login , authenticate 
from vendors.decorators import customer_only , vendor_only
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from vendors.models import VendorItems
from django.utils.decorators import method_decorator
from orders.models import Cart


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

@login_required
@vendor_only
def vendor_profile(request):
	if request.method == 'POST':
		v_form = VendorUpdateForm(request.POST,instance=request.user.v_profile)

		if v_form.is_valid():
			v_form.save()
			messages.success(request , f'Your account has been updated!')
			return redirect('vendor-profile')
	else:
		v_form = VendorUpdateForm(instance=request.user.v_profile)

	context={
		'form':v_form,
		'object_list':VendorItems.objects.filter(item_vendor=request.user,is_listed=True)
	}

	return render(request,'users/vendor_profile.html',context)

@login_required
@customer_only
def customer_profile(request):
	if request.method == 'POST':
		c_form = CustomerUpdateForm(request.POST,instance=request.user.c_profile)
		i_form = CustomerImageForm(request.POST,request.FILES,instance=request.user.c_profile)
		if c_form.is_valid() and i_form.is_valid() :
			c_form.save()
			i_form.save(commit=False)
			messages.success(request , f'Your account has been updated!')
			return redirect('customer-profile')
	else:
		c_form = CustomerUpdateForm(instance=request.user.c_profile)
		i_form = CustomerImageForm()

	context = {
		'c_form':c_form,
		'i_form':i_form
		}
	return render(request,'users/customer_profile.html',context)

def login_redirect(request):
	if request.user.is_vendor and request.user.is_active :
		return redirect('vendor-profile')
		messages.success(request , f'Successfully signed in as {request.user}')
	elif request.user.is_customer and request.user.is_active :
		return redirect('home')
	elif request.user.is_vendor == False and request.user.is_customer == False:
		return redirect('google-login-redirect')

@login_required
@customer_only
def add_money(request):
	if request.method == 'POST':
		m_form = CustomerMoneyForm(request.POST)

		if m_form.is_valid():
			request.user.c_profile.customer_money += m_form.cleaned_data['add_money']
			request.user.c_profile.save()
			messages.success(request , f'Money has been added!')
			return redirect('home')

	else:
		m_form = CustomerMoneyForm()

	return render(request,'users/add_money.html',{'form':m_form})

@login_required
def google_login_redirect(request):
	return render(request,'users/google_login_redirect.html')

@login_required
def make_vendor(request):
	if request.user.is_vendor == False and request.user.is_customer == False:
		user_instance = request.user
		user_instance.is_vendor = True
		user_instance.save()
		VendorProfile.objects.create(vendor_user_profile=request.user)
		return redirect('vendor-profile')
	else:
		return redirect('vendor-profile')


@login_required
def make_customer(request):
	if request.user.is_vendor == False and request.user.is_customer == False:
		user_instance = request.user
		user_instance.is_customer = True
		user_instance.save()
		CustomerProfile.objects.create(customer_user_profile=request.user)
		Cart.objects.create(customer=request.user)
		return redirect('home')
	else:
		return redirect('home')







	
