from django.urls import path
from . import views
 
app_name = 'accounts'
 
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('seller_signup/', views.seller_signup_view, name='seller_signup'),
    path('settings/', views.settings_view, name = 'settings'),
    path('update_user/', views.update_user_view, name='update_user'),
    path('password/', views.change_password, name='change_password'),
    path('payment_card/', views.payment_card_view, name='payment_card'),
    path('add_card/', views.add_card_view, name='add_card')
]