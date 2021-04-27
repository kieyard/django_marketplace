from django import forms

from .models import Product, AddToBasket

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		exclude = ['listedBy', 'item_id']

class AddToBasketForm(forms.ModelForm):
	class Meta:
		model = AddToBasket
		exclude = ['user','product','basket']
