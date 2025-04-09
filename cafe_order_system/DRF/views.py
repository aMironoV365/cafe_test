from rest_framework import viewsets
from orders.models import Product
from .serializers import ProductListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
