from dataclasses import fields
from rest_framework import serializers
from orders.models import Product


class ProductListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product.

    Используется для представления списка продуктов в API.
    Включает только имя и цену продукта.
    """

    class Meta:
        model = Product
        fields = [
            "name",
            "price",
        ]
