from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product

# Create your views here.
def my_products_view(request, *args, **kwargs):
	queryset = Product.objects.all()
	queryset = queryset.filter(listedBy=request.user)

	context = {
		'object_list' : queryset
	}
	return render(request, 'products/product_list.html', context)


def delete_product_view(request, id, *args, **kwargs):
	obj = get_object_or_404(Product, id = id)
	if request.method == 'POST':
		obj.delete()
		return redirect('products:my_products')
	isMyProduct = str(obj.listedBy) == str(request.user)
	context = {
	'object': obj,
	'isMyProduct' : isMyProduct
	}
	return render(request, 'products/product_delete.html', context)

def update_product_view(request, id, *args, **kwargs):
	obj = get_object_or_404(Product, id = id)
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


def product_detail_view(request, id, *args, **kwargs):
	obj = get_object_or_404(Product, id = id)
	isMyProduct = str(obj.listedBy) == str(request.user)
	context = {
	'object' : obj,
	'isMyProduct' : isMyProduct
	}
	return render(request, 'products/product_detail.html', context)