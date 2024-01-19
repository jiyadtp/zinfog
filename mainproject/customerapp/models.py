from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customers(models.Model):
    auth_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, db_index=True)
    name = models.CharField(max_length=100, null=True, db_index=True)
    email = models.CharField(max_length=200, null=True, db_index=True)
    password = models.CharField(max_length=100, null=True, db_index=True)
    phone = models.CharField(max_length=100, null=True, db_index=True)


class Products(models.Model):
    name = models.CharField(max_length=100, null=True, db_index=True)
    product_image = models.FileField(upload_to="product_image", null=True, db_index=True)
    avg_rating = models.IntegerField(null=True, db_index=True)


class Orders(models.Model):
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="customer_order_id",null=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_order_id", null=True)
    order_status = models.CharField(max_length=100, null=True, db_index=True)
    status = models.CharField(max_length=100, null=True, db_index=True)
    total_count = models.CharField(max_length=100, null=True, db_index=True)
    address = models.TextField(null=True, db_index=True)


class OrderAddress(models.Model):
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="customer_order_address_id",null=True)
    address = models.TextField(null=True, db_index=True)

class ProductRating(models.Model):
    customer_id = models.ForeignKey(Customers, on_delete=models.CASCADE, related_name="customer_product_rating_id",null=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="product_product_rating_id", null=True)
    total_rating = models.CharField(max_length=10, null=True, db_index=True)
