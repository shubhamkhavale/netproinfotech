from django.db import models
from apps.invoices.models import Invoice
from apps.payments.models import Payment

class Receipt(models.Model):
    receipt_no = models.CharField(max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.receipt_no
