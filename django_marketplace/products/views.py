from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm, AddToBasketForm
from .models import Product, Basket, AddToBasket

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
	form = AddToBasketForm()
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


def add_to_basket(request, item_id, quantity):
	my_basket, created = Basket.objects.get_or_create(user=request.user)
	obj = get_object_or_404(Product, item_id = item_id)
	entry = AddToBasket.objects.create(user = request.user, product=obj, basket=my_basket, quantity=quantity)
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
	basketItems = AddToBasket.objects.filter(user__exact=request.user)
	basket = get_object_or_404(Basket, user=request.user)
	context={
	'items' : basketItems,
	'basket': basket
	}
	return render(request, 'products/basket.html', context)