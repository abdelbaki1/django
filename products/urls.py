from django.urls import path
from .views import productapi
from .views import getallproduct


urlpatterns = [path('products/create', productapi.as_view()),
               path('products', getallproduct.as_view()),
               path('products/<int:pk>', productapi.as_view()),
               ]
