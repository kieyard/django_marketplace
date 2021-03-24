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