from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Customers)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(OrderAddress)
admin.site.register(ProductRating)
