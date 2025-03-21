from django.urls import path, include
from .views import OrderCreate, OrderList, OrderDetail, OrderUpdate, OrderDelete

app_name = "orders"

urlpatterns = [
    path("orders/create/", OrderCreate.as_view(), name="order_create"),
    path("orders/list/", OrderList.as_view(), name="order_list"),
    path("orders/<int:pk>", OrderDetail.as_view(), name="order_detail"),
    path("orders/<int:pk>/update", OrderUpdate.as_view(), name="order_update"),
    path("orders/<int:pk>/delete", OrderDelete.as_view(), name="order_delete"),
]
