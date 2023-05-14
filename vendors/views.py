from django.shortcuts import render, redirect
from .models import VendorItems
from django.views.generic import ListView , CreateView ,DetailView ,DeleteView ,UpdateView
from users.models import CustomUser
from .decorators import customer_only , vendor_only
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from orders.models import Review ,Order
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import xlwt

@login_required
@customer_only
def ItemListView(request):
	items = VendorItems.objects.filter(is_listed=True)
	context = {'object_list':items}
	return render(request,'vendors/vendoritems_list.html',context)



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


@login_required
@vendor_only
def ItemDeleteView(request,pk):
	item_instance = get_object_or_404(VendorItems , pk=pk)
	item_instance.is_listed = False
	item_instance.save()
	return redirect('vendor-profile')

@login_required
def review_display(request,pk):
	item = get_object_or_404(VendorItems,pk=pk)
	reviews = Review.objects.filter(item_review=item)
	if len(reviews)==0:
		return render(request,'vendors/no_reviews.html')
	else:
		return render(request,'vendors/review_list.html',{'reviews':reviews})

@login_required
@vendor_only
def print_excel(request):
	vendor=request.user
	response = HttpResponse(content_type='application/ms-excel')
	response['Content-Disposition'] = f'attachment; filename={vendor}_orders.xls'

	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet(f'{vendor.v_profile.vendor_name}_orders')
	row_num = 0

	font_style = xlwt.XFStyle()
	font_style.font.bold = True

	columns = ['Customer', 'Item', 'Quantity', 'Total' ]

	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)  


	font_style = xlwt.XFStyle()

	rows = Order.objects.filter(vendor=request.user).values_list('customer__email', 'item_order__item_title', 'quantity_order', 'total_order')
	
	for row in rows:
		row_num += 1
		for col_num in range(len(row)):
			ws.write(row_num, col_num, row[col_num], font_style)

	wb.save(response)
    
	return response




