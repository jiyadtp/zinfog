from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.SignUpApiview.as_view(),name='signup'),
    path('login',views.LoginApiview.as_view(),name='login'),
    path('product-list', views.product_listview),
    path('get-order-details',views.get_order_details,name='get-order-details'),
    ]