from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def home_view(request):
	return redirect('products:product_list')