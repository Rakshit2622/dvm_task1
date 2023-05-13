from django.urls import path
from . import views as vendor_views
from .views import (
	ItemListView,
	ItemDetailView,
	ItemCreateView,
	ItemDeleteView,
	ItemUpdateView
	)


urlpatterns=[
	path('home/',ItemListView.as_view(),name='home'),
	path('list-item/',ItemCreateView.as_view(),name='item-create'),
	path('items/<int:pk>/',ItemDetailView.as_view(),name='item-detail'),
	path('items/<int:pk>/delete',ItemDeleteView.as_view(),name='item-delete'),
	path('items/<int:pk>/update',ItemUpdateView.as_view(),name='item-update'),
	path('items/<int:pk>/review',vendor_views.review_display,name='item-review'),
	path('export/excel',vendor_views.print_excel,name='print-excel')

]