from django.urls import path
from . import views
 
app_name = 'products'
 
urlpatterns = [
    path('create_product/', views.create_product_view, name='create_product'),
]