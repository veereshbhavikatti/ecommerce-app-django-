from rest_framework.views import APIView #create API methods
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product

class CartView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request):
        cart, _=Cart.objects.get_or_create(user=request.user)
        serializer=CartSerializer(cart)
        return Response(serializer.data)
    
class AddToCartView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request):
        product_id= request.data.get('product_id')
        quantity= int(request.data.get('quantity', 1))
        product= get_object_or_404(Product, id= product_id)
        
        if product.stock < quantity:
            return Response(
                {'error': 'Not enough stock'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cart, _= Cart.objects.get_or_create(user=request.user)
            
        # Get or Create Cart
        cart_item, created= CartItem.objects.get_or_create(
            cart=cart, product=product
        )
        
        if not created:
            if product.stock < cart_item.quantity + quantity:
                return Response(
                    {"error": "Stock limit exceeded"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return Response({"message": "Product added to cart"}, status=status.HTTP_200_OK)


class UpdateCartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity'))

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )

        if cart_item.product.stock < quantity:
            return Response(
                {"error": "Not enough stock"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()
        return Response({"message": "Cart updated"})


class RemoveFromCartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        item_id = request.data.get('item_id')

        cart_item = get_object_or_404(
            CartItem,
            id=item_id,
            cart__user=request.user
        )
        cart_item.delete()
        return Response({"message": "Item removed from cart"})
