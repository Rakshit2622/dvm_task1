from django.shortcuts import render ,redirect
from .models import CustomUser,VendorUser,CustomerUser,VendorProfile
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
		'object_list':VendorItems.objects.filter(item_vendor=request.user)
	}

	return render(request,'users/vendor_profile.html',context)

@login_required
@customer_only
def customer_profile(request):
	if request.method == 'POST':
		c_form = CustomerUpdateForm(request.POST,instance=request.user.c_profile)
		i_form = CustomerImageForm(request.POST,request.FILES)
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
	elif request.user.is_customer and request.user.is_active :
		return redirect('home')

@login_required
@customer_only
def add_money(request):
	if request.method == 'POST':
		m_form = CustomerMoneyForm(request.POST)

		if m_form.is_valid():
			money_instance = request.user.c_profile.customer_money
			money_instance += m_form.add_money
			money_instance.save()
			messages.success(request , f'Money has been added!')
			return redirect('home')

	else:
		m_form = CustomerMoneyForm()

	return render(request,'users/add_money.html',{'form':m_form})




	
