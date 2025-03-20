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
    model = Order


class OrderCreate(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_create_form.html'
    success_url = reverse_lazy("orders:order_list")

    def form_valid(self, form):
        """Обработка валидной формы."""
        self.object = form.save(commit=False)  # Создаем объект, но не сохраняем в БД
        self.object.save()  # Сохраняем объект, чтобы получить id

        # Сохраняем связи ManyToMany (продукты)
        form.save_m2m()

        # Пересчитываем total_price (вызовет метод save модели Order)
        self.object.calculate_total_price()
        self.object.save()

        return super().form_valid(form)


class OrderDetail(DetailView):
    queryset = Order.objects.prefetch_related("products")


class OrderUpdate(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = "orders/order_update.html"
    success_url = reverse_lazy("orders:order_list")


class OrderDelete(DeleteView):
    model = Order
    template_name = "orders/order_delete.html"
    success_url = reverse_lazy("orders:order_list")
