from django.urls import path
from .views import (
    SalesReportView,
    PurchaseReportView,
    OutstandingPaymentReportView
)

app_name = 'reports'

urlpatterns = [
    path("sales/", SalesReportView.as_view(), name="sales"),
    path("purchase/", PurchaseReportView.as_view(), name="purchase"),
    path("outstanding/", OutstandingPaymentReportView.as_view(), name="outstanding"),
]
