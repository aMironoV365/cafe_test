from django.db import models


class Table(models.Model):
    number = models.IntegerField(unique=True, verbose_name="Номер стола")
    is_occupied = models.BooleanField(default=False, verbose_name="Занят")

    def __str__(self):
        return f"Стол #{self.number}"

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price} руб."


class Order(models.Model):
    STATUS_CHOICES = [
        ('waiting', 'В ожидании'),
        ('ready', 'Готово'),
        ('paid', 'Оплачено'),
    ]

    table_number = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="orders", verbose_name="Стол")
    products = models.ManyToManyField(Product, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')

    def save(self, *args, **kwargs):
        if self.pk is None:  # Если объект создается впервые
            self.total_price = 0  # Устанавливаем 0, чтобы избежать NULL

        super().save(*args, **kwargs)  # Сохраняем объект, чтобы получить id

        # После сохранения пересчитываем `total_price`, если есть продукты
        if self.products.exists():
            self.total_price = sum(product.price for product in self.products.all())
            super().save(update_fields=["total_price"])
