from rest_framework import viewsets
from orders.models import Product
from .serializers import ProductListSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления продуктами.

    Позволяет выполнять полный CRUD (создание, чтение, обновление, удаление)
    над объектами модели `Product` через API.

    Используемые классы:
    - queryset: все объекты Product
    - serializer_class: сериализатор, определяющий структуру входных/выходных данных
    """

    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
