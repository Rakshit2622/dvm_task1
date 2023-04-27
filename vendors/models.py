from django.db import models
from users.models import CustomUser, VendorUser, VendorProfile
from PIL import Image
from django.urls import reverse

class VendorItems(models.Model):
	item_title = models.CharField(max_length=100)
	item_price = models.PositiveIntegerField()
	item_description = models.CharField(max_length=400)
	item_image = models.ImageField(upload_to='vendor_items_pics')
	item_vendor= models.ForeignKey(CustomUser,on_delete=models.CASCADE)
	item_stock = models.PositiveIntegerField()

	def __str__(self):
		return self.item_title

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.item_image.path)
		output_size=(200,200) 
		img.resize(output_size)
		img.save(self.item_image.path)

	def get_absolute_url(self):
		return reverse('item-detail',kwargs={'pk':self.pk}) 


