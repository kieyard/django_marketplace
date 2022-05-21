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
	return render(request, 'products/my_product_list.html', context)


def delete_product_view(request, item_id, *args, **kwargs):
	obj = get_object_or_404(Product, item_id = item_id)
	if request.method == 'POST':
		obj.delete()
		return redirect('products:my_product_list')
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
			return redirect('products:my_product_list')
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


	queryset = queryset.filter(price__range=(price_min_query, price_max_query))

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
			return redirect('products:my_product_list')

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
	try:	
		my_basket, created = Basket.objects.get_or_create(user=request.user)
	except:
		print()
	try:
		obj = get_object_or_404(Product, item_id = item_id)
	
		if (obj.quantity >= quantity):
			entry = AddToBasket.objects.create(product=obj, basket=my_basket, quantity=quantity)
			my_basket.total += entry.quantity * entry.product.price
			my_basket.item_count += entry.quantity
			my_basket.save()
			return redirect('products:basket')
		else:
			return redirect('products:product_detail', item_id)
	except:
		return redirect('accounts:login')

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






