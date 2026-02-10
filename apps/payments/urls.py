from django.urls import path
from .views import add_payment, payment_list

app_name = 'payments'

urlpatterns = [
    path('', payment_list, name='list'),
    path('add/<int:invoice_id>/', add_payment, name='add'),
]
