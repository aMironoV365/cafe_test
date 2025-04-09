from django.http import HttpResponseRedirect
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
    context_object_name = "order_list"
    queryset = Order.objects.filter(archived=False)


class OrderCreate(CreateView):
    model = Order
    context_object_name = "order_create"
    form_class = OrderForm
    template_name = "orders/order_create_form.html"
    success_url = reverse_lazy("orders:order_list")

    def form_valid(self, form):
        """Обработка валидной формы."""
        self.object = form.save(commit=False)
        self.object.save()

        form.save_m2m()

        self.object.calculate_total_price()
        self.object.save()

        return super().form_valid(form)


class OrderDetail(DetailView):
    queryset = Order.objects.prefetch_related("products")
    context_object_name = "order_details"


class OrderUpdate(UpdateView):
    model = Order
    context_object_name = "order_update"
    form_class = OrderForm
    template_name = "orders/order_update.html"
    success_url = reverse_lazy("orders:order_list")


class OrderDelete(DeleteView):
    model = Order
    context_object_name = "order_delete"
    template_name = "orders/order_delete.html"
    success_url = reverse_lazy("orders:order_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)
