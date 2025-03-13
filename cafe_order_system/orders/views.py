from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Order
from .forms import OrderForm


class OrderList(ListView):
    template_name = "orders/orders_list.html"


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_create_form.html"
    # success_url = reverse_lazy("orders:orders_list")

    def form_valid(self, form):
        """Обработка валидной формы."""
        self.object = form.save(commit=False)
        self.object.save()  # Сохраняем объект (вызовет метод save модели Order)

        # Устанавливаем продукты (total_price будет пересчитан автоматически)
        self.object.products.set(form.cleaned_data['products'])
        return super().form_valid(form)


class OrderDetail(DetailView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderDelete(DetailView):
    pass
