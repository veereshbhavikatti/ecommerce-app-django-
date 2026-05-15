from rest_framework import serializers
from .models import Order, OrderItems

class OrderItemSerializer(serializers.ModelSerializer):
    product_name=serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model= OrderItems
        fields=('product_name','quantity','price')
        
class OrderSerializer(serializers.ModelSerializer):
    items= OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model= Order
        fields=('id', 'total_price','status','created_at','items')