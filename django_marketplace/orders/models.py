from django.db import models
from django.urls import reverse
from accounts.models import CustomUser, Cards, DeliveryAddress
from products.models import Product

import random

# Create your models here.
class Order(models.Model):
	order_id = models.IntegerField(unique=True)
	user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
	seller = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='seller')
	delivery_address = models.ForeignKey(DeliveryAddress, null=True, blank=True, on_delete=models.CASCADE)
	card = models.ForeignKey(Cards, null=True, blank=True, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField()
	total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
	paid_status = models.BooleanField(default=False)
	shipping_status = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	def save(self):
		if self.order_id == None:
			new_id = random.randint(1000000000,9999999999)
			while True:
				try:
					test_unique_id = Order.objects.get(order_id=new_id)
				except Order.DoesNotExist:
					self.order_id = new_id
					break
				else:
					new_id = random.randint(1000000000,9999999999)
					continue
		super(Order, self).save()