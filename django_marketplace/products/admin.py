from django.contrib import admin

# Register your models here.
from .models import Product


class ProductAdmin(admin.ModelAdmin):
	model = Product
	list_display = ('title','description','price')
	fieldsets = (
		(None, {'fields':('item_id', 'title','image','description','price','summary','featured', 'listedBy')}),) 

admin.site.register(Product, ProductAdmin)