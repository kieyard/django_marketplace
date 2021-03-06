from django.urls import path
from . import views
 
app_name = 'orders'
 
urlpatterns = [
    path('create_order/', views.create_order_view, name='create_order'),
    path('<int:order_id>/view_order/', views.view_order_view, name='view_order'),
    path('order_list/', views.order_list_view, name='order_list'),
    path('orders_sold/', views.orders_sold_view, name='orders_sold'),
    path('<int:order_id>/view_sold_order/', views.view_sold_order_view, name='view_sold_order'),
    path('<int:order_id>/mark_order_as_shipped/', views.mark_order_as_shipped, name='mark_order_as_shipped')
]