from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    seller = serializers.ReadOnlyField(source='seller.email')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'image',
            'description',
            'price',
            'stock',
            'is_active',
            'category',
            'category_name',
            'seller',
            'created_at'
        )