import pytest
from django.urls import reverse
from orders.models import Product


@pytest.mark.django_db
class TestProductAPI:
    """
    Набор тестов для API управления продуктами.

    Использует фикстуру `api_client` для выполнения запросов к API.
    """

    def test_create_product(self, api_client):
        """
        Тест создания продукта через POST-запрос к /api/products/

        Проверяется:
        - успешное создание продукта (код 201)
        - продукт действительно сохраняется в базе
        - имя продукта соответствует переданным данным
        """
        url = reverse("product-list")
        data = {"name": "Новый продукт", "price": "250.00"}

        response = api_client.post(url, data, format="json")

        assert response.status_code == 201
        assert Product.objects.count() == 1
        assert Product.objects.first().name == "Новый продукт"

    def test_get_product_list(self, api_client, product1, product2):
        """
        Тест получения списка всех продуктов через GET-запрос к /api/products/

        Проверяется:
        - успешный ответ (код 200)
        - количество продуктов в ответе
        - корректность данных по каждому продукту
        """
        url = reverse("product-list")
        response = api_client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 2
        assert len(data["results"]) == 2
        assert data["results"][0]["name"] == "Кофе"
        assert data["results"][1]["name"] == "Чай"

    def test_get_single_product(self, api_client, product1):
        """
        Тест получения одного продукта по ID через GET-запрос к /api/products/<id>/

        Проверяется:
        - успешный ответ (код 200)
        - корректность полученных данных по продукту
        """
        url = reverse("product-detail", args=[product1.id])
        response = api_client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Кофе"
        assert data["price"] == "150.00"

    def test_update_product(self, api_client, product1):
        """
        Тест обновления продукта по ID через PUT-запрос к /api/products/<id>/

        Проверяется:
        - успешный ответ (код 200)
        - изменения сохраняются в базе
        """
        url = reverse("product-detail", args=[product1.id])
        updated_data = {"name": "Эспрессо", "price": "180.00"}

        response = api_client.put(url, updated_data, format="json")

        assert response.status_code == 200
        product1.refresh_from_db()
        assert product1.name == "Эспрессо"
        assert str(product1.price) == "180.00"

    def test_delete_product(self, api_client, product1):
        """
        Тест удаления продукта по ID через DELETE-запрос к /api/products/<id>/

        Проверяется:
        - успешный ответ (код 204)
        - продукт удалён из базы
        """
        url = reverse("product-detail", args=[product1.id])
        response = api_client.delete(url)

        assert response.status_code == 204
        assert Product.objects.count() == 0
