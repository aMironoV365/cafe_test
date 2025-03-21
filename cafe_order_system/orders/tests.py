from django.test import TestCase, Client
from django.urls import reverse
from .models import Order, Table, Product


class OrderListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, is_occupied=True)
        cls.product = Product.objects.create(name="Маргарита", price=500)
        cls.order = Order.objects.create(status="waiting", table_number=cls.table)
        cls.order.products.add(cls.product)

    def test_order_list_view_status_code(self):
        response = self.client.get(
            reverse("orders:order_list")
        )  # Убедитесь, что в urls.py есть name='order_list'
        self.assertEqual(response.status_code, 200)

    def test_order_list_view_template(self):
        response = self.client.get(reverse("orders:order_list"))
        self.assertTemplateUsed(
            response, "orders/order_list.html"
        )  # Проверьте, что шаблон соответствует вашему

    def test_order_list_view_context(self):
        response = self.client.get(reverse("orders:order_list"))
        self.assertIn("order_list", response.context)
        self.assertEqual(len(response.context["order_list"]), 1)
        self.assertEqual(response.context["order_list"][0].status, "waiting")

    def test_order_total_price_calculation(self):
        self.order.calculate_total_price()
        self.assertEqual(self.order.total_price, 500)


class OrderCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, is_occupied=True)
        cls.product = Product.objects.create(name="Маргарита", price=500)
        cls.order = Order.objects.create(status="waiting", table_number=cls.table)
        cls.order.products.add(cls.product)

    def test_order_create_view_status_code(self):
        # Проверяем, что страница создания заказа доступна
        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)

    def test_order_create_view_uses_correct_template(self):
        # Проверяем, что используется правильный шаблон
        response = self.client.get(reverse("orders:order_create"))
        self.assertTemplateUsed(response, "orders/order_create_form.html")


#
#
# class OrderDetailViewTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.client = Client()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.order.delete()
#         cls.product.delete()
#         cls.table.delete()
#         super().tearDownClass()
#
#
# class OrderUpdateViewTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.client = Client()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.order.delete()
#         cls.product.delete()
#         cls.table.delete()
#         super().tearDownClass()
#
#
# class OrderDeleteViewTest(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.client = Client()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.product.delete()
#         cls.table.delete()
#         super().tearDownClass()
