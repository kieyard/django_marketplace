from django.contrib import admin

# Register your models here.
from .models import Product, Basket, AddToBasket, Order, OrderItem


class ProductAdmin(admin.ModelAdmin):
	model = Product
	list_display = ('item_id','title','description','price')
	fieldsets = (
		(None, {'fields':('item_id', 'title','image','description','price','summary', 'quantity','featured', 'listedBy')}),) 

admin.site.register(Product, ProductAdmin)





class AddToBasketInLine(admin.TabularInline):
	model = AddToBasket
	extra = 0


class BasketAdmin(admin.ModelAdmin):
	model = Basket
	list_display = ('user',)
	fieldsets = (
		(None, {'fields':('user','item_count','total')}),)
	inlines = [AddToBasketInLine]



admin.site.register(Basket, BasketAdmin)



class OrderItemInLine(admin.TabularInline):
	model = OrderItem
	extra = 0


class OrderAdmin(admin.ModelAdmin):
	model = Order
	list_display = ('order_id',)
	fieldsets = (
		(None, {'fields':('order_id', 'user', 'delivery_address', 'card')}),)
	inlines = [OrderItemInLine]



admin.site.register(Order, OrderAdmin)