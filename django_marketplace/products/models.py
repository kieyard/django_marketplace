from django.db import models
from django.urls import reverse
from accounts.models import CustomUser

from django.db.models.signals import post_save

import random


# Create your models here.
class Product(models.Model):
	item_id = models.IntegerField(unique=True)
	title = models.CharField(max_length=120) 
	image = models.ImageField(upload_to='images', blank=True)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=10000)
	summary = models.TextField(blank=False,null=False)
	featured = models.BooleanField()
	listedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('products:product_detail', kwargs={'item_id': self.item_id})

	def save(self):
		new_id = random.randint(1000000000,9999999999)
		while True:
			try:
				test_unique_id = Product.objects.get(item_id=new_id)
			except Product.DoesNotExist:
				self.item_id = new_id
				break
			else:
				new_id = random.randint(1000000000,9999999999)
				continue
		super(Product, self).save()