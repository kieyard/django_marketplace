from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProductForm
from .models import Product

# Create your views here.
def create_product_view(request, *args, **kwargs):
	form = ProductForm()
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		form.instance.listedBy = request.user
		if form.is_valid():
			form.save()

	context = {
		'form' : form
	}
	return render(request, 'products/create_product.html', context)