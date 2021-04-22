from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm, StripeConnectSetupForm, AddCardSetupForm, AddDeliveryAddressForm
from .models import CustomUser, DeliveryAddress, Cards
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages

import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
import time

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
	obj = CustomUser.objects.get(email=request.user.email)
	if obj.is_seller == False:
		data = {'email': obj.email, 'first_name': obj.first_name, 'last_name': obj.last_name}
		form = StripeConnectSetupForm(initial=data)
		if request.method == 'POST':
			form = StripeConnectSetupForm(request.POST, request.FILES)
			if form.is_valid() and form.cleaned_data['accept_TOS']:
				idf = stripe.File.create(
					purpose="identity_document",
					file=form.cleaned_data['identity_document_front']
				)
				idb = stripe.File.create(
					purpose="identity_document",
					file=form.cleaned_data['identity_document_back']
				)
				addi = stripe.File.create(
					purpose="identity_document",
					file=form.cleaned_data['additional_ID']
				)
				
				account = stripe.Account.create(
					type="custom",
					country=form.cleaned_data['country'],
					email=form.cleaned_data['email'],
					capabilities={
						"card_payments": {"requested": True},
						"transfers": {"requested": True},
					},
					business_type='individual',
					individual = {
						"address":{
							"city": form.cleaned_data['city'],
							"country": form.cleaned_data['country'],
							"line1": form.cleaned_data['address_line_1'],
							"line2": form.cleaned_data['address_line_2'],
							"postal_code": form.cleaned_data['postal_code']
						},
						"dob":{
							"day": form.cleaned_data['DOB'].day,
							"month": form.cleaned_data['DOB'].month,
							"year":form.cleaned_data['DOB'].year
						},
						"email": form.cleaned_data['email'],
						"first_name":form.cleaned_data['first_name'],
						"last_name":form.cleaned_data['last_name'],
						"phone": form.cleaned_data['phone'],
						"verification":{
							"document":{
								"front": idf.id,
								"back": idb.id,
							},
							"additional_document":{
								"front": addi.id,
							},
						},
					},
					business_profile={
						'mcc': '4225',
						'url': 'djangomarket.com'
					},
					external_account = {
						'object': 'bank_account',
						'country': form.cleaned_data['country'],
						'currency': 'GBP',
						'account_holder_name': form.cleaned_data['first_name'] + form.cleaned_data['last_name'],
						'routing_number': form.cleaned_data['payout_sort_code'] ,
						'account_number': form.cleaned_data['payout_account_number'] ,
					},
					tos_acceptance={
						'date': int(time.time()),
						'ip': '8.8.8.8',
					}
				)

				obj = CustomUser.objects.get(email=request.user.email)
				obj.stripe_seller_id = account.id
				obj.stripe_seller_TOS_accepted = True
				obj.is_seller = True
				obj.save()

		context = {
			'form' : form
		}

		return render(request, 'accounts/seller_signup.html', context)

	elif obj.is_seller == True:
		return redirect('products:create_product')



def settings_view(request):
	return render(request, 'accounts/settings.html')


def update_user_view(request):
	obj = CustomUser.objects.get(email=request.user.email)
	form = CustomUserChangeForm(instance=obj)
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, request.FILES, instance=obj)
		if form.is_valid():
			obj = form.save()
			return redirect('accounts:update_user')
	context = {
		'form': form
	}
	return render(request, 'accounts/update_user.html', context)


def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('accounts:change_password')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'accounts/change_password.html', {
		'form': form
	})


def add_card_view(request):
	form = AddCardSetupForm()
	if request.method == 'POST':
		form = AddCardSetupForm(request.POST, request.FILES)
		if form.is_valid():
			tok = stripe.Token.create(
				card={
					'number' : form.cleaned_data['card_number'],
					'exp_month' : form.cleaned_data['exp_month'],
					'exp_year' : form.cleaned_data['exp_year'],
					'cvc' : form.cleaned_data['cvc'],
				},
			)
			
			pm = stripe.PaymentMethod.create(
				type="card",
				card={'token':tok.id},
			)
			
			stripe.PaymentMethod.attach(
				pm.id,
				customer=request.user.stripe_customer_id,
			)
			Cards.objects.get_or_create(user=request.user, card_id=pm.id, last_4=pm.card.last4, brand=pm.card.brand)
			return redirect('accounts:settings')

	context = {
		'form' : form
	}

	return render(request, 'accounts/add_card.html', context)

def add_delivery_address_view(request):
	form = AddDeliveryAddressForm()
	if request.method == 'POST':
		form = AddDeliveryAddressForm(request.POST, request.FILES)
		form.instance.user = request.user
		if form.is_valid():
			form.save()
			return redirect('accounts:settings')

	context = {
		'form' : form
	}
	return render(request, 'accounts/add_delivery_address.html', context)

