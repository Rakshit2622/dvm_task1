from django.shortcuts import render, redirect
from .models import Cart , Order ,Review
from vendors.models import VendorItems
from django.contrib.auth.decorators import login_required
from vendors.decorators import customer_only , vendor_only
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from .forms import ReviewForm

@login_required
@customer_only
def add_to_cart(request,pk):
	item = get_object_or_404(VendorItems , pk=pk)
	vendor = item.item_vendor
	cart_instance = request.user.cart_customer
	total = item.item_price
	if cart_instance.full == True and cart_instance.item.id != item.pk :
		messages.error(request,f'You can add only one type of item in the cart')
		return redirect('home')
	elif cart_instance.full == True and cart_instance.item.id == item.pk:
		if cart_instance.quantity + 1 > item.item_stock:
			messages.error(request,f'This amount of qty doesnt exist in the stock')
			return redirect('home')
		else:
			cart_instance.quantity += 1
			cart_instance.total = cart_instance.quantity * cart_instance.item.item_price
			cart_instance.save()
			messages.success(request,f'Item quantity increased in the cart')
			return redirect('home')
	elif cart_instance.quantity + 1 > item.item_stock:
		messages.error(request,f'This amount of qty doesnt exist in the stock')
		return redirect('home')
	else:
		cart_instance.vendor = vendor
		cart_instance.item = item
		cart_instance.total = total
		cart_instance.quantity +=1
		cart_instance.full = True
		cart_instance.save()
		messages.success(request,f'Item has been added')
		return redirect('home')

@login_required
@customer_only
def cart_list(request):
	if request.user.cart_customer.full == True:
		return render(request,'orders/cart_list.html')
	else:
		return render(request,'orders/empty_cart.html')

@login_required
@customer_only
def remove_from_cart(request):
	cart_instance = request.user.cart_customer
	cart_instance.vendor = None
	cart_instance.item = None
	cart_instance.total = 0
	cart_instance.quantity = 0
	cart_instance.full = False
	cart_instance.save()
	return redirect('home')


@login_required
@customer_only
def order(request):
	cart_instance = request.user.cart_customer
	vendor = request.user.cart_customer.vendor
	customer = request.user
	item_order = cart_instance.item
	quantity_order = cart_instance.quantity
	total_order = cart_instance.total

	if customer.c_profile.customer_address == '# Enter Your Address here':
		messages.error(request,f'Please add your address in the profile section ')
		return redirect('home')
	else:
		address = customer.c_profile.customer_address

	if customer.c_profile.customer_money < total_order:
		messages.error(request,f'You dont have enough money')
	else:
		money_instance = request.user.c_profile
		item_instance = cart_instance.item
		item_instance.item_orders +=1
		item_instance.item_stock -= quantity_order
		money_instance.customer_money -= total_order
		money_instance.save()
		item_instance.save()
		messages.success(request,f'Your order has been placed')
		Order.objects.create(vendor=vendor,customer=customer,item_order=item_order,quantity_order=quantity_order,total_order=total_order,address=address)
		cart_instance.vendor = None
		cart_instance.item = None
		cart_instance.total = 0
		cart_instance.quantity = 0
		cart_instance.full = False
		cart_instance.save()

	return redirect('cart_list')

@login_required
@customer_only
def order_customer_view(request):
	orders = Order.objects.filter(customer=request.user)
	return render(request,'orders/customer_orders.html',{'orders':orders})

@login_required
@vendor_only
def order_vendor_view(request):
	orders = Order.objects.filter(vendor=request.user)
	return render(request,'orders/vendor_orders.html',{'orders':orders})

@method_decorator([login_required,customer_only], name='dispatch')
class OrderDetailView(DetailView):
	model = Order


def ReviewCreateView(request,pk):
	if request.method == 'POST':
		form = ReviewForm(request.POST)
		item = get_object_or_404(VendorItems , pk=pk)

		if form.is_valid():
			form.instance.customer_review = request.user
			form.instance.item_review = item
			form.save()
			messages.success(request , f'Reviw successfully posted!')
			return redirect('home')
	else:
		form = ReviewForm()

	context={
		'form':form
	}

	return render(request,'orders/review.html',context)



		






