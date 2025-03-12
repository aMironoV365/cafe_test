from django.core.management.base import BaseCommand
from orders.models import Table


class Command(BaseCommand):
    help = "Loads 20 tables into the database"

    def handle(self, *args, **options):
        self.stdout.write("Creating tables...")

        # Создаем 20 столиков
        for table_number in range(1, 21):  # Номера столов от 1 до 20
            table, created = Table.objects.get_or_create(number=table_number)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created table: {table.number}"))
            else:
                self.stdout.write(self.style.WARNING(f"Table already exists: {table.number}"))

        self.stdout.write(self.style.SUCCESS("Tables loaded successfully!"))
