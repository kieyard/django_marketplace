from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, StripeSellerSignupForm
from .models import CustomUser
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm

import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

def signup_view(request, *args, **kwargs):
	form = CustomUserCreationForm()
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('accounts:signup')

	context = {
		'form': form
	}
	return render(request, 'accounts/signup.html', context)


def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('accounts:login')
	else:
		form = AuthenticationForm()

	context = {
	'form' : form
	}
	return render(request, 'accounts/login.html', context)


def logout_view(request):
	logout(request)
	return redirect('accounts:login')


def seller_signup_view(request, *args, **kwargs):
	form = StripeSellerSignupForm()
	if request.method == 'POST':
		form =StripeSellerSignupForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			return redirect('accounts:login')

	context = {
		'form': form
	}
	return render(request, 'accounts/seller_signup.html', context)

def seller_signup(request):
	account = stripe.Account.create(
		type="custom",
		country="GB",
		email=request.user,
		capabilities={
			"card_payments": {"requested": True},
			"transfers": {"requested": True},
		},
	)
	print(account.id)
	form = StripeSellerSignupForm()
	form.stripe_seller_id = account.id
	if form.is_valid():
			user = form.save()
	print(form.is_valid())

	return redirect('accounts:login')