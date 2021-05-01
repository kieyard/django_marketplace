from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm, AddToBasketForm
from .models import Product, Basket, AddToBasket, Category
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
	price_min_query = request.GET.get('price_min')
	price_max_query = request.GET.get('price_max')
	try:
		category_query = Category.objects.get(category = request.GET.get('category'))
	except Category.DoesNotExist:
		category_query = ''

	if price_min_query is None or price_min_query == '':
		price_min_query = 0.00
	if price_max_query is None or price_max_query == '':
		arg = Product.objects.all().order_by('-price').first()
		price_max_query = arg.price

	if title_search_query != '' and title_search_query is not None:
		queryset = queryset.filter(title__icontains=title_search_query).filter(price__range=(price_min_query, price_max_query))
	if category_query != '' and category_query is not None:
		queryset = queryset.filter(category=category_query)
	

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
	if (obj.quantity >= quantity):
		entry = AddToBasket.objects.create(product=obj, basket=my_basket, quantity=quantity)
		my_basket.total += entry.quantity * entry.product.price
		my_basket.item_count += entry.quantity
		my_basket.save()
		return redirect('products:basket')
	else:
		return redirect('products:product_detail', item_id)

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
				
			return redirect('products:order_list')

	context = {
		'form' : form,
		'items' : basketItems,
		'basket': basket
	}
	return render(request, 'products/create_order.html', context)


def view_order_view(request, order_id):
	order = get_object_or_404(Order, order_id__exact=order_id)

	context={
	'order': order,
	}
	return render(request, 'products/view_order.html', context)

def order_list_view(request):
	orders = Order.objects.filter(user=request.user).order_by('-created')
	context = {
	'orders': orders,
	}

	return render(request, 'products/order_list.html', context)



