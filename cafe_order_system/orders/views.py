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
    """
    Представление для отображения списка заказов.

    Контролирует отображение всех заказов, которые не архивированы.
    Использует фильтрацию по полю `archived` (false).

    Атрибуты:
        model: Модель, с которой работает представление (Order).
        context_object_name: Имя контекста для списка заказов.
        queryset: Запрос для получения всех неархивированных заказов.
    """

    model = Order
    context_object_name = "order_list"
    queryset = Order.objects.filter(archived=False)


class OrderCreate(CreateView):
    """
    Представление для создания нового заказа.

    Формирует форму для создания нового заказа. После того как форма отправлена и валидирована,
    создаётся новый объект заказа, вычисляется его общая стоимость, и он сохраняется в базе данных.

    Атрибуты:
        model: Модель, с которой работает представление (Order).
        context_object_name: Имя контекста для отображаемой формы.
        form_class: Класс формы для создания заказа.
        template_name: Шаблон для отображения формы.
        success_url: URL, куда происходит редирект после успешного создания заказа.

    Методы:
        form_valid: Обработка валидной формы — сохраняет заказ, вычисляет его общую стоимость
                    и перенаправляет на страницу списка заказов.
    """

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
    """
    Представление для отображения подробностей заказа.

    Отображает подробную информацию о выбранном заказе, включая все связанные продукты.

    Атрибуты:
        queryset: Запрос для получения заказа с предзагруженными связанными продуктами.
        context_object_name: Имя контекста для отображаемых данных заказа.
    """

    queryset = Order.objects.prefetch_related("products")
    context_object_name = "order_details"


class OrderUpdate(UpdateView):
    """
    Представление для редактирования заказа.

    Обрабатывает обновление данных существующего заказа. Пользователь может изменить информацию о заказе,
    включая статус и продукты. После успешного обновления заказ сохраняется.

    Атрибуты:
        model: Модель, с которой работает представление (Order).
        context_object_name: Имя контекста для отображаемой формы.
        form_class: Класс формы для редактирования заказа.
        template_name: Шаблон для отображения формы.
        success_url: URL, куда происходит редирект после успешного обновления заказа.
    """

    model = Order
    context_object_name = "order_update"
    form_class = OrderForm
    template_name = "orders/order_update.html"
    success_url = reverse_lazy("orders:order_list")


class OrderDelete(DeleteView):
    """
    Представление для удаления (архивации) заказа.

    После подтверждения удаления заказ архивируется (помечается как архивный),
    и происходит перенаправление на страницу списка заказов.

    Атрибуты:
        model: Модель, с которой работает представление (Order).
        context_object_name: Имя контекста для отображаемого заказа.
        template_name: Шаблон для отображения страницы удаления.
        success_url: URL, куда происходит редирект после успешного удаления.

    Методы:
        form_valid: Обработка валидной формы — заказ архивируется и перенаправляется на список заказов.
    """

    model = Order
    context_object_name = "order_delete"
    template_name = "orders/order_delete.html"
    success_url = reverse_lazy("orders:order_list")

    def form_valid(self, form):
        """Архивирует заказ и перенаправляет на страницу списка заказов."""
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)
