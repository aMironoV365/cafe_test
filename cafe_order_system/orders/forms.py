from django import forms
from .models import Order, Product


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказов.

    Позволяет выбрать номер стола, блюда (множество продуктов) и статус заказа.
    Поле `products` переопределено для отображения в виде флажков (checkbox).
    """

    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите блюда",
    )

    class Meta:
        model = Order
        fields = ["table_number", "products", "status"]
