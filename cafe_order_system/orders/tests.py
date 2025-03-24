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
        response = self.client.get(reverse("orders:order_list"))
        self.assertEqual(response.status_code, 200)

    def test_order_list_view_template(self):
        response = self.client.get(reverse("orders:order_list"))
        self.assertTemplateUsed(response, "orders/order_list.html")

    def test_order_list_view_context(self):
        response = self.client.get(reverse("orders:order_list"))
        order_from_context = response.context["order_list"][0]

        self.assertIn("order_list", response.context)
        self.assertEqual(len(response.context["order_list"]), 1)
        self.assertEqual(order_from_context.id, self.order.id)

        self.assertEqual(order_from_context.status, "waiting")

        # 5. Проверка связанного стола
        self.assertEqual(
            order_from_context.table_number.id, self.table.id
        )  # Проверяем id стола
        self.assertEqual(
            order_from_context.table_number.number, 1
        )  # Проверяем номер стола

        # 6. Проверка продуктов в заказе
        products_in_order = order_from_context.products.all()
        self.assertEqual(products_in_order.count(), 1)  # Проверяем количество продуктов
        self.assertEqual(
            products_in_order[0].id, self.product.id
        )  # Проверяем id продукта
        self.assertEqual(products_in_order[0].name, "Маргарита")  # Проверяем название

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
        response = self.client.get(reverse("orders:order_create"))
        self.assertEqual(response.status_code, 200)

    def test_order_create_view_uses_correct_template(self):
        response = self.client.get(reverse("orders:order_create"))
        self.assertTemplateUsed(response, "orders/order_create_form.html")


class OrderDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, is_occupied=True)
        cls.product = Product.objects.create(name="Маргарита", price=500)
        cls.order = Order.objects.create(status="waiting", table_number=cls.table)
        cls.order.products.add(cls.product)

    def test_product_get(self):
        response = self.client.get(
            reverse("orders:order_detail", args=(self.order.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_correct_template(self):
        response = self.client.get(
            reverse("orders:order_detail", args=(self.order.id,))
        )
        self.assertTemplateUsed(response, "orders/order_detail.html")

    def test_detail_view_context(self):
        response = self.client.get(
            reverse("orders:order_detail", args=(self.order.id,))
        )
        self.assertIn("order_details", response.context)
        self.assertEqual(response.context["order_details"].id, self.order.id)
        self.assertEqual(response.context["order_details"].status, "waiting")
        self.assertEqual(response.context["order_details"].table_number, self.table)
        self.assertIn(self.product, response.context["order_details"].products.all())


class OrderUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, is_occupied=True)
        cls.product = Product.objects.create(name="Маргарита", price=500)
        cls.order = Order.objects.create(status="waiting", table_number=cls.table)
        cls.order.products.add(cls.product)

    def test_update_view_statuscode(self):
        response = self.client.get(
            reverse("orders:order_update", args=(self.order.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_update_view_correct_template(self):
        response = self.client.get(
            reverse("orders:order_update", args=(self.order.id,))
        )
        self.assertTemplateUsed(response, "orders/order_update.html")

    def test_update_view_context(self):
        response = self.client.get(
            reverse("orders:order_update", args=(self.order.id,))
        )
        self.assertIn("order_update", response.context)
        self.assertEqual(response.context["order_update"].id, self.order.id)
        self.assertEqual(response.context["order_update"].status, "waiting")
        self.assertEqual(response.context["order_update"].table_number, self.table)
        self.assertIn(self.product, response.context["order_update"].products.all())


class OrderDeleteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.table = Table.objects.create(number=1, is_occupied=True)
        cls.product = Product.objects.create(name="Маргарита", price=500)
        cls.order = Order.objects.create(status="waiting", table_number=cls.table)
        cls.order.products.add(cls.product)

    def test_delete_view_status_code(self):
        response = self.client.get(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_view_correct_template(self):
        response = self.client.get(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.assertTemplateUsed(response, "orders/order_delete.html")

    def test_delete_view_context(self):
        response = self.client.get(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.assertIn("order_delete", response.context)
        self.assertEqual(response.context["order_delete"].id, self.order.id)
        self.assertEqual(response.context["order_delete"].status, "waiting")
        self.assertEqual(response.context["order_delete"].table_number, self.table)
        self.assertIn(self.product, response.context["order_delete"].products.all())
    
    def test_delete_order_post_request(self):
        response = self.client.post(
            reverse("orders:order_delete", args=(self.order.id,))
        )
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())
        self.assertRedirects(response, reverse("orders:order_list"))
