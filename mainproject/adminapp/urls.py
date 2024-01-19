from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        path('',views.admin_login,name='admin-login'),
        path('login-check',views.login_check,name='login-check'),

        path('dashboard', views.dashboard, name='dashboard'),
        path('customers', views.customers, name='customers'),
        path('products', views.products, name='products'),
        path('create-product', views.create_product, name='create-product'),
        path('edit-product', views.edit_product, name='edit-product'),
        path('edit-product-action',views.edit_product_action,name='edit-product-action'),
        path('delete-product/<int:id>', views.delete_product, name='delete-product'),
        path('orders', views.orders, name='orders'),

        path('change-status',views.change_status,name='change-status'),

        path('', auth_views.LogoutView.as_view(), name="logout"),
    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)