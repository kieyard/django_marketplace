from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, StripeConnectSetup, AddCardSetup
from django import forms

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('email', 'first_name', 'last_name')

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ('email','first_name', 'last_name')


class StripeConnectSetupForm(forms.ModelForm):
	class Meta:
		model = StripeConnectSetup
		fields = ('__all__')

class AddCardSetupForm(forms.ModelForm):
	class Meta:
		model = AddCardSetup
		fields = ('__all__')