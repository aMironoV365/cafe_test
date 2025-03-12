from django.urls import path, include
from .views import OrderCreate
app_name = "orders"

urlpatterns = [
    path("orders/create/", OrderCreate.as_view(), name="order_create"),
    # path("Orders/list/", )
]
