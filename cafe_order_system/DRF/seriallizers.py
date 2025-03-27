from dataclasses import fields
from rest_framework import serializers
from orders.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
        ]
