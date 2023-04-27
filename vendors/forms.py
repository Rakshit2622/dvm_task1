from django import forms
from .models import VendorItems

class ItemCreateForm(forms.ModelForm):
	class Meta:
		model = VendorItems
		fields = ["item_title","item_price","item_description","item_image"]