from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=120) 
	image = models.ImageField(upload_to='images', blank=True)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=10000)
	summary = models.TextField(blank=False,null=False)
	featured = models.BooleanField()
	listedBy = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.title
