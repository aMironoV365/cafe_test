from django.shortcuts import render
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework import viewsets
from orders.models import Product
from .seriallizers import ProductListSerializer


class ProductViewSet(CacheResponseMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    list_cache_timeout = 300
    object_cache_timeout = 600
