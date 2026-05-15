from django.db import models
from django.conf import settings
from products.models import Product

User = settings.AUTH_USER_MODEL

class Order(models.Model):
    STATUS_CHOICES=(
        ('PENDING','Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED','Cancelled'),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"order #{self.id}"
    
class OrderItems(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name}({self.quantity})"