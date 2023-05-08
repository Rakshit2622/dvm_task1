from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from PIL import Image
from .managers import UserManager ,VendorManager,CustomerManager
from django.contrib import admin

class CustomUser(AbstractBaseUser):
	email = models.EmailField(max_length=250,unique=True)
	is_active=models.BooleanField(default=True)
	is_admin=models.BooleanField(default=False)
	is_staff=models.BooleanField(default=False)
	is_superuser=models.BooleanField(default=False)
	
	is_customer = models.BooleanField(default=False)
	is_vendor = models.BooleanField(default=False)

	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS= []

	objects = UserManager()

	def __str__(self):
		return str(self.email)

	def has_perm(self,perm,obj=None):
		return self.is_admin

	def has_module_perms(self,app_label):
		return True

	def save(self,*args,**kwargs):
		return super().save(*args,**kwargs)

class VendorUser(CustomUser):
	objects = VendorManager()

	class Meta:
		proxy = True
	
	def save(self,*args,**kwargs):
		if not self.id or self.id==None:
			self.is_customer =False
			self.is_vendor = True
		return super().save(*args,**kwargs)

class CustomerUser(CustomUser):
	objects = CustomerManager()

	class Meta:
		proxy = True
	
	def save(self,*args,**kwargs):
		if not self.id or self.id==None:
			self.is_customer =True
			self.is_vendor = False
		return super().save(*args,**kwargs)

class VendorProfile(models.Model):
	vendor_user_profile = models.OneToOneField(VendorUser, related_name='v_profile' ,on_delete=models.CASCADE)
	vendor_name = models.CharField(max_length=100,blank=True,null=True)
	vendor_phone_no = models.PositiveIntegerField(blank=True,null=True)

	def __str__(self):
		return f'{self.vendor_user_profile.email} VendorProfile'

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
        



class CustomerProfile(models.Model):
	customer_user_profile = models.OneToOneField(CustomerUser, related_name='c_profile' ,on_delete=models.CASCADE)
	customer_name = models.CharField(max_length=100)
	customer_address = models.TextField(default = '# Enter Your Address here')
	customer_money = models.PositiveIntegerField(default=0,null=True)
	customer_image = models.ImageField(default='default.jpeg',upload_to='customer_profile_pics')

	def __str__(self):
		return f'{self.customer_user_profile.email} VendorProfile'

	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
		img = Image.open(self.customer_image.path)
		if img.height>300 or img.width>300:
			output_size=(300,300) 
			img.thumbnail(output_size)
			img.save(self.customer_image.path)




		
