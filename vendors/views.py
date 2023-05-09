from django.shortcuts import render, redirect
from .models import VendorItems
from django.views.generic import ListView , CreateView ,DetailView ,DeleteView ,UpdateView
from users.models import CustomUser
from .decorators import customer_only , vendor_only
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from orders.models import Review
from django.shortcuts import get_object_or_404

@method_decorator([login_required,customer_only] , name='dispatch')
class ItemListView(ListView):
	model = VendorItems
	ordering = ['-item_orders']

@method_decorator([login_required,vendor_only] , name='dispatch')
class ItemCreateView(CreateView):
	model = VendorItems
	fields = ['item_title','item_description','item_price','item_stock','item_image']

	def form_valid(self , form):
		form.instance.item_vendor = self.request.user
		form.save()
		return super(ItemCreateView , self).form_valid(form)

	
@method_decorator(login_required , name='dispatch')
class ItemDetailView(DetailView):
	model = VendorItems

@method_decorator([login_required,vendor_only] , name='dispatch')
class ItemUpdateView(UserPassesTestMixin,UpdateView):
	model = VendorItems
	fields = ['item_title','item_description','item_price','item_stock','item_image']


	def form_valid(self , form):
		form.instance.item_vendor = self.request.user
		form.save()
		return super(ItemUpdateView , self).form_valid(form)

	def test_func(self):
		item = self.get_object()
		if self.request.user == item.item_vendor:
			return True
		else:
			False


@method_decorator([login_required,vendor_only], name = 'dispatch')
class ItemDeleteView(UserPassesTestMixin,DeleteView):
	model = VendorItems
	success_url = 'vendor-profile/'

	def test_func(self):
		item = self.get_object()
		if self.request.user == item.item_vendor:
			return True
		else:
			False


def review_display(request,pk):
	item = get_object_or_404(VendorItems,pk=pk)
	reviews = Review.objects.filter(item_review=item)
	if len(reviews)==0:
		return render(request,'vendors/no_reviews.html')
	else:
		return render(request,'vendors/review_list.html',{'reviews':reviews})



