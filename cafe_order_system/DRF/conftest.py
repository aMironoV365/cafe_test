import pytest
from rest_framework.test import APIClient
from orders.models import Product, Order, Table


@pytest.fixture
def api_client():
    """Фикстура для API-клиента."""
    return APIClient()


@pytest.fixture
def table(db):
    """Фикстура для создания стола."""
    return Table.objects.create(number=1, is_occupied=False)


@pytest.fixture
def product1(db):
    """Фикстура для создания первого тестового продукта."""
    return Product.objects.create(name="Кофе", price=150.00)


@pytest.fixture
def product2(db):
    """Фикстура для создания второго тестового продукта."""
    return Product.objects.create(name="Чай", price=100.00)


@pytest.fixture
def order(db, table, product1, product2):
    """Фикстура для создания заказа с продуктами."""
    order = Order.objects.create(table_number=table, status="waiting")
    order.products.set([product1, product2])  # Добавляем продукты в заказ
    order.calculate_total_price()  # Обновляем стоимость заказа
    order.save()
    return order
