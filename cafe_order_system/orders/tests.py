from django.test import TestCase
from django.urls import reverse
from .models import Order, Table, Product


class BaseTestCase(TestCase):
    """
    Базовый класс для тестов заказов.

    Подготавливает общие объекты:
    - Стол с номером 1
    - Продукт "Маргарита" с ценой 500
    - Заказ со статусом "waiting", не архивирован, привязан к столу и продукту
    Используется всеми другими классами тестов через наследование.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        """Создаёт тестовые данные один раз для всех тестов."""
        cls.table = Table.objects.create(number=1, is_occupied=True)
        cls.product = Product.objects.create(name="Маргарита", price=500)
        cls.order = Order.objects.create(
            status="waiting", table_number=cls.table, archived=False
        )
        cls.order.products.add(cls.product)


class OrderListViewTest(BaseTestCase):
    """
    Тесты для представления списка заказов (order_list).
    Проверяет доступность, шаблон, корректность контекста и расчёт цены.
    """

    def test_order_list_view_status_code(self) -> None:
        """Проверяет, что страница списка заказов возвращает статус 200."""
        response = self.client.get(reverse("orders:order_list"))
        self.assertEqual(response.status_code, 200)

    def test_order_list_view_template(self) -> None:
        """Проверяет, что используется правильный шаблон order_list.html."""
        response = self.client.get(reverse("orders:order_list"))
        self.assertTemplateUsed(response, "orders/order_list.html")

    def test_order_list_view_context(self) -> None:
        """
        Проверяет, что в контексте передаётся список заказов.
        Список содержит один заказ с ожидаемыми полями: статус, стол, продукт.
        """
        response = self.client.get(reverse("orders:order_list"))
        order_from_context = response.context["order_list"][0]

        self.assertIn("order_list", response.context)
        self.assertEqual(len(response.context["order_list"]), 1)
        self.assertEqual(order_from_context.id, self.order.id)
        self.assertEqual(order_from_context.status, "waiting")
        self.assertEqual(order_from_context.table_number.id, self.table.id)
        self.assertEqual(order_from_context.table_number.number, 1)

        products_in_order = order_from_context.products.all()
        self.assertEqual(products_in_order.count(), 1)
        self.assertEqual(products_in_order[0].id, self.product.id)
        self.assertEqual(products_in_order[0].name, "Маргарита")

    def test_order_total_price_calculation(self) -> None:
        """Проверяет корректность метода calculate_total_price."""
        self.order.calculate_total_price()
        self.assertEqual(self.order.total_price, 500)


class OrderCreateViewTest(BaseTestCase):
    """
    Тесты представления создания заказа (order_create).
    Проверяет доступность страницы и использование правильного шаблона.
    """

    def test_order_create_view_status_code(self) -> None:
        """Проверяет, что страница создания заказа возвращает статус 200."""
        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)

    def test_order_create_view_uses_correct_template(self) -> None:
        """Проверяет, что используется шаблон order_create_form.html."""
        response = self.client.get(reverse("orders:order_create"))
        self.assertTemplateUsed(response, "orders/order_create_form.html")


class OrderDetailViewTest(BaseTestCase):
    """
    Тесты представления деталей заказа (order_detail).
    Проверяет статус ответа, шаблон и содержимое контекста.
    """

    def test_product_get(self) -> None:
        """Проверяет, что GET-запрос к detail-странице возвращает статус 200."""
        response = self.client.get(
            reverse("orders:order_detail", args=(self.order.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_correct_template(self) -> None:
        """Проверяет, что используется шаблон order_detail.html."""
        response = self.client.get(
            reverse("orders:order_detail", args=(self.order.id,))
        )
        self.assertTemplateUsed(response, "orders/order_detail.html")

    def test_detail_view_context(self) -> None:
        """
        Проверяет, что в контексте передаются детали нужного заказа:
        статус, стол и связанные продукты.
        """
        response = self.client.get(
            reverse("orders:order_detail", args=(self.order.id,))
        )
        self.assertIn("order_details", response.context)
        self.assertEqual(response.context["order_details"].id, self.order.id)
        self.assertEqual(response.context["order_details"].status, "waiting")
        self.assertEqual(response.context["order_details"].table_number, self.table)
        self.assertIn(self.product, response.context["order_details"].products.all())


class OrderUpdateViewTest(BaseTestCase):
    """
    Тесты представления обновления заказа (order_update).
    Проверяет доступность, шаблон и содержимое контекста.
    """

    def test_update_view_statuscode(self) -> None:
        """Проверяет, что страница обновления возвращает статус 200."""
        response = self.client.get(
            reverse("orders:order_update", args=(self.order.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_correct_template(self) -> None:
        """Проверяет, что используется шаблон order_update.html."""
        response = self.client.get(
            reverse("orders:order_update", args=(self.order.id,))
        )
        self.assertTemplateUsed(response, "orders/order_update.html")

    def test_update_view_context(self) -> None:
        """
        Проверяет, что контекст содержит нужный заказ
        со всеми его полями и связанными продуктами.
        """
        response = self.client.get(
            reverse("orders:order_update", args=(self.order.id,))
        )
        self.assertIn("order_update", response.context)
        self.assertEqual(response.context["order_update"].id, self.order.id)
        self.assertEqual(response.context["order_update"].status, "waiting")
        self.assertEqual(response.context["order_update"].table_number, self.table)
        self.assertIn(self.product, response.context["order_update"].products.all())


class OrderDeleteViewTest(BaseTestCase):
    """
    Тесты представления удаления (архивации) заказа (order_delete).
    Проверяет отображение, шаблон, контекст и обработку POST-запроса.
    """

    def test_delete_view_status_code(self) -> None:
        """Проверяет, что страница удаления заказа возвращает статус 200."""
        response = self.client.get(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_view_correct_template(self) -> None:
        """Проверяет, что используется шаблон order_delete.html."""
        response = self.client.get(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.assertTemplateUsed(response, "orders/order_delete.html")

    def test_delete_view_context(self) -> None:
        """
        Проверяет, что в контексте передан нужный заказ с верными атрибутами
        и связанными продуктами.
        """
        response = self.client.get(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.assertIn("order_delete", response.context)
        self.assertEqual(response.context["order_delete"].id, self.order.id)
        self.assertEqual(response.context["order_delete"].status, "waiting")
        self.assertEqual(response.context["order_delete"].table_number, self.table)
        self.assertIn(self.product, response.context["order_delete"].products.all())

    def test_delete_order_post_request(self) -> None:
        """
        Проверяет, что POST-запрос к удалению архивирует заказ и
        перенаправляет на страницу списка заказов.
        """
        response = self.client.post(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.order.refresh_from_db()
        self.assertTrue(self.order.archived)
        self.assertRedirects(response, reverse("orders:order_list"))
