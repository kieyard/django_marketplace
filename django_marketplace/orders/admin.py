from django.contrib import admin
from .models import Order
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
	model = Order
	list_display = ('order_id','user','product','created')
	fieldsets = (
		(None, {'fields':('order_id', 'user','seller', 'delivery_address', 'card', 'product','quantity','total','paid_status','shipping_status','created')}),)
	readonly_fields = ['created',]



admin.site.register(Order, OrderAdmin)