from django.urls import path
from . import views
 
app_name = 'accounts'
 
urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view,name='logout'),
    path('seller_signup/', views.seller_signup_view, name='seller_signup'),
    path('setup_stripe_connect/', views.setup_stripe_connect, name = 'setup_stripe_connect'),
    path('settings/', views.settings_view, name = 'settings'),
    path('update_user/', views.update_user_view, name='update_user')
]