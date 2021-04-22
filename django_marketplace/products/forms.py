from django import forms

from .models import Product, AddToBasket, Order

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		exclude = ['listedBy', 'item_id']

class AddToBasketForm(forms.ModelForm):
	class Meta:
		model = AddToBasket
		exclude = ['user','product','basket']

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude = ['order_id','user','item_count','total']
		