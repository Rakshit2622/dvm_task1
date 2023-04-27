from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
	def create_user(self,email,password=None):
		if not email:
			raise ValueError('The email must be set')
		if not password:
			raise ValueError('Password is must!')
		email = self.normalize_email(email)
		user = self.model(email = email)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,password):
		user = self.create_user(
            email = self.normalize_email(email) , 
            password = password
        )
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using = self._db)
		return user

class VendorManager(BaseUserManager):
	def create_user(self,email,password=None):
		if not email:
			raise ValueError('The email must be set')
		if not password:
			raise ValueError('Password is must!')
		email = self.normalize_email(email)
		user = self.model(email = email)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def get_queryset(self,*args,**kwargs):
		return super(VendorManager, self).get_queryset(*args,**kwargs).filter(is_vendor=True)

class CustomerManager(BaseUserManager):
	def create_user(self,email,password=None):
		if not email:
			raise ValueError('The email must be set')
		if not password:
			raise ValueError('Password is must!')
		email = self.normalize_email(email)
		user = self.model(email = email)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def get_queryset(self,*args,**kwargs):
		return super(CustomerManager, self).get_queryset(*args,**kwargs).filter(is_customer=True)

