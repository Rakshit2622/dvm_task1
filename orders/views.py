from django.shortcuts import render, redirect
from .models import Cart , Order ,Review ,Cart , Cart_Items ,Wishlist
from vendors.models import VendorItems
from django.contrib.auth.decorators import login_required
from vendors.decorators import customer_only , vendor_only
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView ,DeleteView
from django.utils.decorators import method_decorator
from .forms import ReviewForm
from django.core.mail import send_mail

@login_required
@customer_only
def add_to_cart(request,pk):
	item = get_object_or_404(VendorItems , pk=pk)
	cart_instance = request.user.cart_customer
	if request.user.cart_customer.cart_end.all() :
		if str(item) in list(Cart_Items.objects.filter(customer=request.user).values_list('item__item_title',flat=True)) :
			cart_item_instance = Cart_Items.objects.get(item=item , customer=request.user)
			if cart_item_instance.quantity + 1 > item.item_stock:
				messages.error(request,f'This amount of qty doesnt exist in the stock')
				return redirect('home')
			else:
				cart_item_instance.quantity+=1
				cart_item_instance.total += item.item_price
				cart_item_instance.save()
				messages.success(request,f'Item quantity increased in the cart')
				return redirect('home')
		else:
			if item.item_stock > 0:
				cart_instance.save()
				Cart_Items.objects.create(item=item,vendor=item.item_vendor,customer=request.user,quantity=1,total=item.item_price,cart=request.user.cart_customer)
				messages.success(request,f'Item added in the cart')
				return redirect('home')
			else:
				messages.error(request,f'This amount of qty doesnt exist in the stock')
				return redirect('home')

	else:
		if item.item_stock > 0:
			Cart_Items.objects.create(item=item,vendor=item.item_vendor,customer=request.user,quantity=1,total=item.item_price,cart=request.user.cart_customer)
			messages.success(request,f'Item added in the cart')
			return redirect('home')
		else:
			messages.error(request,f'This amount of qty doesnt exist in the stock')
			return redirect('home')

@login_required
@customer_only
def cart_list(request):
	if request.user.cart_customer.cart_end.all():
		cart_items = Cart_Items.objects.filter(customer=request.user)
		context = {
		'cart_items':cart_items,
		'bill_amt': request.user.cart_customer.get_bill_amt()
		}
		return render(request,'orders/cart_list.html',context)
	else:
		return render(request,'orders/empty_cart.html')

@login_required
@customer_only
def remove_from_cart(request):
	Cart_Items.objects.all().delete()
	return redirect('home')

@method_decorator([login_required,customer_only], name='dispatch')
class CartItemDeleteView(DeleteView):
	model = Cart_Items
	success_url = '/cart/'


@login_required
@customer_only
def order(request):
	customer = request.user
	if customer.c_profile.customer_money < customer.cart_customer.get_bill_amt():
		messages.error(request,f'You dont have enough money for the order')
		return redirect('home')

	elif customer.c_profile.customer_address == '# Enter Your Address here' or None:
		messages.error(request,f'Please add your address in the profile section ')
		return redirect('home')

	else:
		for order_item in Cart_Items.objects.filter(customer=customer):
			cart_item_instance = order_item
			vendor = cart_item_instance.vendor
			quantity_order = cart_item_instance.quantity
			total_order = cart_item_instance.total
			address = customer.c_profile.customer_address
			money_instance = request.user.c_profile
			item_instance = cart_item_instance.item
			item_instance.item_orders +=1
			item_instance.item_stock -= quantity_order
			money_instance.customer_money -= total_order
			money_instance.save()
			item_instance.save()
			messages.success(request,f'Your order has been placed')
			Order.objects.create(vendor=vendor,customer=customer,item_order=order_item.item,quantity_order=quantity_order,total_order=total_order,address=address)
			send_mail(
				f'Order For You for the item {cart_item_instance.item}',
				f'You have an order for the item {cart_item_instance.item} :\nQuantity-{cart_item_instance.quantity}\nTotal bill amount-{cart_item_instance.total}\nCustomer Address- {customer.c_profile.customer_address}',
				"f20220471@pilani.bits-pilani.ac.in",
				[f'{cart_item_instance.vendor}'],
				fail_silently=False,
			)
			cart_item_instance.delete()
			return redirect('home')


@login_required
@customer_only
def order_customer_view(request):
	orders = Order.objects.filter(customer=request.user).order_by('-date_time_order')
	return render(request,'orders/customer_orders.html',{'orders':orders})

@login_required
@vendor_only
def order_vendor_view(request):
	orders = Order.objects.filter(vendor=request.user).order_by('-date_time_order')
	return render(request,'orders/vendor_orders.html',{'orders':orders})


@method_decorator([login_required,customer_only], name='dispatch')
class OrderDetailView(DetailView):
	model = Order
	

@login_required
@customer_only
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


@login_required
@customer_only
def add_to_wishlist(request,pk):
	item = get_object_or_404(VendorItems,pk=pk)
	customer = request.user
	if Wishlist.objects.filter(customer=customer):
		if str(item) in list(Wishlist.objects.filter(customer=request.user).values_list('item__item_title',flat=True)) :
			messages.error(request,f'Item already in the wishlist')
		else:
			Wishlist.objects.create(wishlist_item=item,customer=customer)
			messages.success(request,f'Item added in Wishlist')
			return redirect('home')
	else:
		Wishlist.objects.create(wishlist_item=item,customer=customer)
		messages.success(request,f'Item added in Wishlist')
		return redirect('home')

@login_required
@customer_only
def move_to_cart(request,pk):
	item = get_object_or_404(VendorItems,pk=pk)
	add_to_cart(request,item.id)
	Wishlist.objects.get(wishlist_item=item,customer=request.user).delete()
	return redirect('home')

@login_required
@customer_only
def wishlist_list(request):
	customer = request.user
	if Wishlist.objects.filter(customer=customer):
		wishlist_items = Wishlist.objects.filter(customer=customer)
		context = {'wishlist_items':wishlist_items}
		return render(request,'orders/wishlist.html',context)
	else:
		return render(request,'orders/empty_wishlist.html')


@login_required
@customer_only
def remove_wishlist(request):
	Wishlist.objects.all().delete()
	messages.success(request,f'Wishlist has been deleted')
	return redirect('home')

@method_decorator([login_required,customer_only], name='dispatch')
class WishlistDeleteView(DeleteView):
	model = Wishlist
	success_url = '/wishlist/'
	success_message = f'Item has been deleted from wishlist'







		






