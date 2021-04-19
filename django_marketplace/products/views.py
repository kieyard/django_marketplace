from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm, AddToBasketForm, OrderForm
from .models import Product, Basket, AddToBasket, Order, OrderItem
from accounts.models import DeliveryAddress, Cards

# Create your views here.
def my_products_view(request, *args, **kwargs):
	queryset = Product.objects.all()
	queryset = queryset.filter(listedBy=request.user)

	context = {
		'object_list' : queryset
	}
	return render(request, 'products/product_list.html', context)


def delete_product_view(request, item_id, *args, **kwargs):
	obj = get_object_or_404(Product, item_id = item_id)
	if request.method == 'POST':
		obj.delete()
		return redirect('products:my_products')
	isMyProduct = str(obj.listedBy) == str(request.user)
	context = {
	'object': obj,
	'isMyProduct' : isMyProduct
	}
	return render(request, 'products/product_delete.html', context)

def update_product_view(request, item_id, *args, **kwargs):
	obj = get_object_or_404(Product, item_id = item_id)
	form = ProductForm(request.POST or None, instance = obj)
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES, instance = obj)
		if form.is_valid():
			form.save()
			return redirect('products:my_products')
	isMyProduct = str(obj.listedBy) == str(request.user)
	context = {
	'form' : form,
	'isMyProduct' : isMyProduct
	}
	return render(request, 'products/update_product.html', context)

def product_list_view(request, *args, **kwargs):
	queryset = Product.objects.all()
	title_search_query = request.GET.get('title_search')

	if title_search_query != '' and title_search_query is not None:
		queryset = queryset.filter(title__icontains=title_search_query)

	context = {
		'object_list' : queryset
	}
	return render(request, 'products/product_list.html', context)

def create_product_view(request, *args, **kwargs):
	form = ProductForm()
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		form.instance.listedBy = request.user
		if form.is_valid():
			form.save()
			return redirect('products:my_products')

	context = {
		'form' : form
	}
	return render(request, 'products/create_product.html', context)


def product_detail_view(request, item_id, *args, **kwargs):
	obj = get_object_or_404(Product, item_id = item_id)
	isMyProduct = str(obj.listedBy) == str(request.user)
	form = AddToBasketForm(initial={'quantity': 1,})
	if request.method == 'POST':
		form = AddToBasketForm(request.POST, request.FILES)
		if form.is_valid():
			quantity = request.POST['quantity']
			return redirect('products:add_to_basket', item_id, quantity)
	context = {
	'object' : obj,
	'isMyProduct' : isMyProduct,
	'form' : form
	}
	return render(request, 'products/product_detail.html', context)


def add_to_basket(request, item_id, quantity=1):
	my_basket, created = Basket.objects.get_or_create(user=request.user)
	obj = get_object_or_404(Product, item_id = item_id)
	entry = AddToBasket.objects.create(product=obj, basket=my_basket, quantity=quantity)
	my_basket.total += entry.quantity * entry.product.price
	my_basket.item_count += entry.quantity
	my_basket.save()
	return redirect('products:basket')

def delete_add_to_basket_entry(request, id):
	my_basket = get_object_or_404(Basket, user=request.user)
	query = get_object_or_404(AddToBasket, id = id)
	my_basket.total -= query.quantity * query.product.price
	my_basket.item_count -= query.quantity
	query.delete()
	my_basket.save()
	return redirect('products:basket')

def basket_view(request):
	basketItems = AddToBasket.objects.filter(basket__user__exact=request.user)
	basket = get_object_or_404(Basket, user=request.user)
	context={
	'items' : basketItems,
	'basket': basket
	}
	return render(request, 'products/basket.html', context)

def create_order_view(request):
	basketItems = AddToBasket.objects.filter(basket__user__exact=request.user)
	basket = get_object_or_404(Basket, user=request.user)
	form = OrderForm()
	form.fields['delivery_address'].queryset = DeliveryAddress.objects.filter(user=request.user)
	form.fields['card'].queryset = Cards.objects.filter(user=request.user)
	if request.method == 'POST':
		form = OrderForm(request.POST, request.FILES)
		form.instance.user = request.user
		form.fields['delivery_address'].queryset = DeliveryAddress.objects.filter(user=request.user)
		form.fields['card'].queryset = Cards.objects.filter(user=request.user)
		if form.is_valid():
			form.save()
			order_id=form.instance.order_id
			return redirect('products:create_order_and_order_items', order_id)

	context = {
		'form' : form,
		'items' : basketItems,
		'basket': basket
	}
	return render(request, 'products/create_order.html', context)

def create_order_and_order_items(request, order_id):
	basket = get_object_or_404(Basket, user=request.user)
	basketItems = AddToBasket.objects.filter(basket__user__exact=request.user)
	for item in basketItems:
		order = get_object_or_404(Order, order_id=order_id)
		order_item, created = OrderItem.objects.get_or_create(order_id=order, product=item.product, quantity=item.quantity)

	for item in basketItems:
		item.delete()

	basket.item_count = 0
	basket.total = 0
	basket.save()

	return redirect('products:view_order', order_id=order_id)


def view_order_view(request, order_id):
	order = get_object_or_404(Order, order_id__exact=order_id)
	order_items = OrderItem.objects.filter(order_id=order)

	context={
	'order': order,
	'order_items' : order_items,
	
	}
	return render(request, 'products/view_order.html', context)



