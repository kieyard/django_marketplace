from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
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

def seller_signup_view(request):
	return render(request, 'accounts/seller_signup.html')

def setup_stripe_connect(request, *args, **kwargs):
	obj = CustomUser.objects.get(email=request.user.email)

	if obj.stripe_seller_id == '' or None:

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

		obj.stripe_seller_id = account.id
		obj.is_seller = True
		obj.save()

	return redirect('accounts:seller_signup')

def settings_view(request):
	return render(request, 'accounts/settings.html')

def update_user_view(request):
	form = CustomUserChangeForm()
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, request.FILES)
		if form.is_valid():
			obj = CustomUser.objects.get(email=request.user.email)
			obj.email = form.cleaned_data['email']
			obj.first_name = form.cleaned_data['first_name']
			obj.last_name = form.cleaned_data['last_name']
			obj.save()
			return redirect('accounts:update_user')

	context = {
		'form': form
	}
	return render(request, 'accounts/update_user.html', context)

import time
def accept_stripe_TOS(request):
	obj = CustomUser.objects.get(email=request.user.email)

	stripe.Account.modify(
		obj.stripe_seller_id,
		tos_acceptance={
		'date': int(time.time()),
		'ip': '8.8.8.8', # Depends on what web framework you're using
		}
	)

	obj.stripe_seller_TOS_accepted = True
	obj.save()

	return redirect('accounts:seller_signup')





