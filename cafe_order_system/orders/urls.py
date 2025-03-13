from django.urls import path, include
from .views import OrderCreate, OrderList
app_name = "orders"

urlpatterns = [
    path("orders/create/", OrderCreate.as_view(), name="order_create"),
    path("orders/list/", OrderList.as_view(), name="order_list"),

]
