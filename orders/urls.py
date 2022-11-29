from django.urls import path
from .views import GetAllOrder
from .views import GetanOrder
from .views import ExportAPIView
from .views import ChartAPIView
from .views import CreateOrder


urlpatterns = [
    path('orders', GetAllOrder.as_view()),
    path('orders/<int:pk>', GetanOrder.as_view()),
    path('orders/export', ExportAPIView.as_view()),
    path('orders/import', CreateOrder.as_view()),
    path('orders/chart', ChartAPIView.as_view())]
