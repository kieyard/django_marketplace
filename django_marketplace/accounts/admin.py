from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, DeliveryAddress, Cards

from products.models import Product, Basket, AddToBasket
from orders.models import Order

class DeliveryAddressesInLine(admin.TabularInline):
	model = DeliveryAddress
	extra = 0

class CardsInline(admin.TabularInline):
	model = Cards
	extra = 0

class ProductInLine(admin.TabularInline):
	model = Product
	extra = 1
	show_change_link = True

class BasketInLine(admin.TabularInline):
	model = Basket
	extra = 0
	show_change_link = True


class OrderInLine(admin.TabularInline):
	model = Order
	extra = 0
	show_change_link = True
	fk_name = 'user'

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ('email', 'is_seller', 'is_buyer',)
	list_filter = ('email', 'is_seller', 'is_buyer',)
	fieldsets = (
		(None, {'fields': ('email', 'password', 'first_name', 'last_name', 'date_joined')}),
		('Stripe', {'fields':('stripe_customer_id', 'stripe_seller_id','stripe_seller_TOS_accepted',)}),
		('Permissions', {'fields': ( 'is_buyer', 'is_seller', 'is_staff', 'is_active')}),
	)
	inlines = [CardsInline, DeliveryAddressesInLine, OrderInLine, ProductInLine, BasketInLine]
	add_fieldsets = (
		(None, {
			'classes': ('wide', ),
			'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_seller', 'is_buyer')
			}),
		)
	search_fields = ('email',)
	ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
