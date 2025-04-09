from django.core.management.base import BaseCommand
from orders.models import Product


class Command(BaseCommand):
    help = "Loads initial products into the database"

    def handle(self, *args, **options):
        self.stdout.write("Creating products...")

        products_data = [
            {"name": "Пицца Маргарита", "price": 450.00},
            {"name": "Пицца Пепперони", "price": 500.00},
            {"name": "Салат Цезарь", "price": 350.00},
            {"name": "Борщ", "price": 300.00},
            {"name": "Чай", "price": 100.00},
            {"name": "Кофе", "price": 150.00},
        ]

        for product_data in products_data:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Product already exists: {product.name}"))

        self.stdout.write(self.style.SUCCESS("Products loaded successfully!"))
