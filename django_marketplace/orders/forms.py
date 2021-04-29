from django import forms

from .models import Order

class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		exclude = ['order_id','user','product','quantity','total','paid_status','created']
		
class MarkAsShippedForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['shipping_status']