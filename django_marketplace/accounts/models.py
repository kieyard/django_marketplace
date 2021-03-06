from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager

from django.db.models.signals import post_save
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	is_buyer = models.BooleanField(default=True)
	is_seller = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(default=timezone.now)
	stripe_customer_id = models.CharField(max_length=40)
	stripe_seller_id = models.CharField(max_length=40, default= '')
	stripe_seller_TOS_accepted = models.BooleanField(default=False)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.email

def post_save_create(sender, instance, created, *args, **kwargs):
	if created:
		CustomUser.objects.get_or_create(email=instance)

	user, created = CustomUser.objects.get_or_create(email=instance)

	if user.stripe_customer_id is None or user.stripe_customer_id == '':
		new_stripe_customer_id = stripe.Customer.create(email=instance.email)
		user.stripe_customer_id = new_stripe_customer_id['id']
		user.save()

post_save.connect(post_save_create, sender=settings.AUTH_USER_MODEL)

class Cards(models.Model):
	user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
	card_id = models.CharField(max_length=40, null=True)
	last_4 = models.CharField(max_length=4, null=True)
	brand = models.CharField(max_length=40)

	def __str__(self):
		return (self.brand + ' - ' + self.last_4)

class DeliveryAddress(models.Model):
	user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=40, null = True)
	last_name = models.CharField(max_length=40, null = True)
	address_line_1 = models.CharField(max_length=100, null = True)
	address_line_2 = models.CharField(max_length=100, null = True)
	city = models.CharField(max_length=100, null = True)
	postal_code = models.CharField(max_length=7, null = True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name + ' ' + self.address_line_1 + ' ' + self.address_line_2 + ' ' + self.city + ' ' + self.postal_code 

class StripeConnectSetup(models.Model):
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	email = models.EmailField()
	DOB = models.DateField(auto_now=False,auto_now_add=False)
	phone = models.CharField(max_length=13)
	#business_types = ['individual','company',]
	#business_type=models.CharField(max_length=20, choices=business_types)
	address_line_1 = models.CharField(max_length=100)
	address_line_2 = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=3)
	postal_code = models.CharField(max_length=7)
	identity_document_front = models.ImageField(upload_to='images',blank=True)
	identity_document_back = models.ImageField(upload_to='images',blank=True)
	additional_ID = models.ImageField(upload_to='images',blank=True)
	payout_sort_code = models.CharField(max_length=6)
	payout_account_number = models.CharField(max_length=8)
	accept_TOS = models.BooleanField()
	
class AddCardSetup(models.Model):
	card_holders_fullname = models.CharField(max_length=80)
	card_number = models.CharField(max_length=16)
	exp_month = models.IntegerField()
	exp_year = models.IntegerField()
	cvc = models.IntegerField()



