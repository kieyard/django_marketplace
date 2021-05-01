from django.contrib import admin

# Register your models here.
from .models import Product, Basket, AddToBasket, Category


class ProductAdmin(admin.ModelAdmin):
	model = Product
	list_display = ('item_id','title','description','price')
	fieldsets = (
		(None, {'fields':('item_id', 'title','image','description','price','category','summary', 'quantity','featured', 'listedBy')}),) 

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


class CategoryAdmin(admin.ModelAdmin):
	model = Category
	list_display = ('category',)
	fieldsets = (
		(None, {'fields':('category',)}),)


admin.site.register(Category, CategoryAdmin)