from django.shortcuts import render, get_object_or_404, redirect
from .forms import OrderForm, MarkAsShippedForm
from .models import Order
from accounts.models import DeliveryAddress, Cards
from products.models import Basket, AddToBasket

# Create your views here.
def create_order_view(request):
	basketItems = AddToBasket.objects.filter(basket__user__exact=request.user)
	basket = get_object_or_404(Basket, user=request.user)
	
	form = OrderForm()
	form.instance.user=request.user
	form.fields['delivery_address'].queryset = DeliveryAddress.objects.filter(user=request.user)
	form.fields['card'].queryset = Cards.objects.filter(user=request.user)
	
	if request.method == 'POST':
		form = OrderForm(request.POST, request.FILES)
		form.instance.user=request.user
		form.fields['delivery_address'].queryset = DeliveryAddress.objects.filter(user=request.user)
		form.fields['card'].queryset = Cards.objects.filter(user=request.user)
		
		if form.is_valid():
			for item in basketItems:
				if (item.product.quantity >= item.quantity):
					continue
				else:
					basket.item_count -= item.quantity
					basket.total -= item.product.price * item.quantity
					basket.save()
					item.delete()
					return redirect('products:basket')

			for item in basketItems: 
				form.instance.user=request.user
				form.instance.seller = item.product.listedBy
				form.instance.product = item.product
				form.instance.quantity = item.quantity
				form.instance.total = item.product.price * item.quantity
			
				form.save()
				form = form = OrderForm(request.POST, request.FILES)
				
				item.product.quantity -= item.quantity
				item.product.save()

			for item in basketItems:
				item.delete()

			basket.item_count = 0
			basket.total = 0
			basket.save()
				
			return redirect('orders:order_list')

	context = {
		'form' : form,
		'items' : basketItems,
		'basket': basket
	}
	return render(request, 'orders/create_order.html', context)


def view_order_view(request, order_id):
	order = get_object_or_404(Order, order_id__exact=order_id)

	context={
	'order': order,
	}
	return render(request, 'orders/view_order.html', context)

def order_list_view(request):
	orders = Order.objects.filter(user=request.user).order_by('-created')
	context = {
	'orders': orders,
	}

	return render(request, 'orders/order_list.html', context)


def orders_sold_view(request):
	orders = Order.objects.filter(seller=request.user).order_by('-created')
	context = {
	'orders': orders,
	}

	return render(request, 'orders/orders_sold.html', context)


def view_sold_order_view(request, order_id):
	order = get_object_or_404(Order, order_id__exact=order_id)
	form = MarkAsShippedForm(instance=order)
	if request.method == 'POST':
		form = MarkAsShippedForm(request.POST, request.FILES, instance=order)
		if form.is_valid():
			order = form.save()
			return redirect('orders:orders_sold')

	context={
	'order': order,
	'form': form,
	}
	return render(request, 'orders/view_sold_order.html', context)

