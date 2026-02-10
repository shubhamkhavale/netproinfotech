from django.urls import path
from .views import receipt_pdf, receipt_list

app_name = 'receipts'

urlpatterns = [
    path('', receipt_list, name='list'),
    path('pdf/<int:receipt_id>/', receipt_pdf, name='pdf'),
]
