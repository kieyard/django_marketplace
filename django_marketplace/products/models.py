from django.db import models
from django.urls import reverse
from accounts.models import CustomUser, Cards, DeliveryAddress

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

import random

class Category(models.Model):
	category = models.CharField(max_length=120)
	def __str__(self):
		return self.category

class Product(models.Model):
	item_id = models.IntegerField(unique=True)
	title = models.CharField(max_length=120) 
	image = models.ImageField(upload_to='images', blank=True)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=10000)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	summary = models.TextField(blank=False,null=False)
	quantity = models.PositiveIntegerField()
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

class Basket(models.Model):
	user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
	item_count = models.PositiveIntegerField(default=0)
	total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)

class AddToBasket(models.Model):
	product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
	basket = models.ForeignKey(Basket, null = True, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()












