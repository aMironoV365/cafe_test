from django import forms
from .models import Order, Product


class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите блюда",
    )

    class Meta:
        model = Order
        fields = ["table_number", "products", "status"]
