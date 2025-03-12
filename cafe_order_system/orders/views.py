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
        self.object = form.save(commit=False)
        self.object.total_price = 0  # Устанавливаем 0 перед первым сохранением
        self.object.save()  # Теперь у объекта есть id

        # Устанавливаем продукты и пересчитываем `total_price`
        self.object.products.set(form.cleaned_data['products'])
        self.object.total_price = sum(product.price for product in self.object.products.all())
        self.object.save()

        return super().form_valid(form)


class OrderDetail(DetailView):
    pass


class OrderUpdate(UpdateView):
    pass


class OrderDelete(DetailView):
    pass
