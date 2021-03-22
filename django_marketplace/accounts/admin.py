from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ('email', 'is_seller', 'is_buyer',)
	list_filter = ('email', 'is_seller', 'is_buyer',)
	fieldsets = (
		(None, {'fields': ('email', 'password', 'date_joined')}),
		('Permissions', {'fields': ('is_staff', 'is_active', 'is_seller', 'is_buyer')}),
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide', ),
			'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_seller', 'is_buyer')
			}),
		)
	search_fields = ('email',)
	ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)