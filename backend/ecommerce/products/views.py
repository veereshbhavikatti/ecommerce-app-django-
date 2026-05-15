from rest_framework import generics, permissions
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsSeller
from rest_framework.parsers import MultiPartParser,FormParser

# category
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser]
        return [permissions.AllowAny()]
    
# product
class ProductListView(generics.ListAPIView):
    queryset= Product.objects.filter(is_active=True)
    serializer_class=ProductSerializer
    permission_classes=[permissions.AllowAny]

# product create

class ProductCreateView(generics.CreateAPIView):
    serializer_class=ProductSerializer
    permission_classes=[IsSeller]
    parser_classes=(MultiPartParser, FormParser)
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsSeller()]
        return [permissions.AllowAny()]