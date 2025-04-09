import pytest
from rest_framework.test import APIClient
from orders.models import Product, Order, Table


@pytest.fixture
def api_client() -> APIClient:
    """
    Фикстура для API-клиента.

    Возвращает:
        APIClient: Тестовый клиент для отправки HTTP-запросов к DRF-представлениям.
    """
    return APIClient()


@pytest.fixture
def table(db) -> Table:
    """
    Фикстура для создания тестового стола.

    Использует встроенную фикстуру `db` для доступа к базе данных.

    Возвращает:
        Table: Экземпляр модели Table с номером 1 и флагом `is_occupied=False`.
    """
    return Table.objects.create(number=1, is_occupied=False)


@pytest.fixture
def product1(db) -> Product:
    """
    Фикстура для создания первого тестового продукта.

    Возвращает:
        Product: Продукт с именем "Кофе" и ценой 150.00.
    """
    return Product.objects.create(name="Кофе", price=150.00)


@pytest.fixture
def product2(db) -> Product:
    """
    Фикстура для создания второго тестового продукта.

    Возвращает:
        Product: Продукт с именем "Чай" и ценой 100.00.
    """
    return Product.objects.create(name="Чай", price=100.00)


@pytest.fixture
def order(db, table: Table, product1: Product, product2: Product) -> Order:
    """
    Фикстура для создания тестового заказа с двумя продуктами.

    Аргументы:
        table (Table): Тестовый стол.
        product1 (Product): Первый тестовый продукт.
        product2 (Product): Второй тестовый продукт.

    Возвращает:
        Order: Заказ, связанный с переданным столом и продуктами, с вычисленной общей стоимостью.
    """
    order = Order.objects.create(table_number=table, status="waiting")
    order.products.set([product1, product2])
    order.calculate_total_price()
    order.save()
    return order
