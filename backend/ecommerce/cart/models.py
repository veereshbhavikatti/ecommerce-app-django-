from django.db import models
from django.conf import settings
from products.models import Product

User= settings.AUTH_USER_MODEL

class Cart(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'cart of {self.user}'
    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    
    # Prevents duplicate products in same cart
    class Meta:
         unique_together=('cart', 'product')
         
         def __str__(self):
                return f'{self.product.name}({self.quantity})'