from rest_framework import serializers
from customerapp.models import Customers,Products,Orders

class ProductSerializer(serializers.ModelSerializer):
    image_path = serializers.SerializerMethodField()
    class Meta:
        model = Products
        fields = [
            'pk',
            'name',
            'image_path'
        ]

    def get_image_path(self, obj):
        if str(obj.product_image):
            return "media/" + str(obj.product_image)
        else:
            return None


class OrderDetails(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()
    class Meta:
        model = Orders
        fields = [
            'pk',
            'customer_id',
            'customer_name',
            'product_id',
            'product_name',
            'order_status',
            'status',
            'total_count',
            'address'
        ]

    def get_customer_name(self, obj):
        try:
            return obj.customer_id.name
        except:
            return None

    def get_product_name(self, obj):
        try:
            return obj.product_id.name
        except:
            return None