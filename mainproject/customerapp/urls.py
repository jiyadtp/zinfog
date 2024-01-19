from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('',views.index,name='index'),
        path('login-check-customer',views.login_check_customer,name='login-check-customer'),
        path('sign-up',views.sign_up,name='sign-up'),
        path('register-data',views.register_data,name='register-data'),

        path('customer-product',views.customer_products,name='customer-product'),
        path('cart',views.cart,name='cart'),
        path('add-to-cart',views.add_to_cart,name='add-to-cart'),
        path('buy-now',views.buy_now,name='buy-now'),
        path('delete-order/<int:id>', views.delete_order, name='delete-order'),

        path('customer-orders', views.customer_orders, name='customer-orders'),

        path('rate-product',views.rate_products,name='rate-product'),

        path('', auth_views.LogoutView.as_view(), name="customer-logout"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)