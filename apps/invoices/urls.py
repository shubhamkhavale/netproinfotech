from django.urls import path
from .views import create_invoice, invoice_detail, invoice_list
from .pdf import invoice_pdf

app_name = "invoices"

urlpatterns = [
    path('', invoice_list, name='list'),
    # Support creating an invoice without a path arg; quotation id may be
    # supplied as a GET parameter (e.g. ?quotation=123). This avoids
    # NoReverseMatch when templates try to reverse a no-arg URL.
    path('create/', create_invoice, name='create_noarg'),
    path('create/<int:quotation_id>/', create_invoice, name='create'),
    path('<int:pk>/', invoice_detail, name='detail'),
    path('<int:pk>/pdf/', invoice_pdf, name='pdf'),
]
