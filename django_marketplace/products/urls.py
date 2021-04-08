from django.urls import path
from . import views
 
app_name = 'products'
 
urlpatterns = [
	path('<int:id>/', views.product_detail_view, name = 'product_detail'),
    path('<int:id>/update_product/', views.update_product_view, name = 'update_product'),
    path('<int:id>/delete_product/', views.delete_product_view, name = 'delete_product'),
    path('create_product/', views.create_product_view, name = 'create_product'),
    path('product_list/', views.product_list_view, name = 'product_list'),
    path('my_products_list/', views.my_products_view, name = 'my_products'),
]