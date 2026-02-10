from django.urls import path
from .views import product_list, product_create

app_name = 'products'

urlpatterns = [
    path('', product_list, name='list'),
    path('create/', product_create, name='create'),
]
