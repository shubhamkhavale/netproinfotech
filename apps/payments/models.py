from django.db import models
from apps.invoices.models import Invoice

class Payment(models.Model):
    PAYMENT_MODE = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque'),
    )

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='payments'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Payment ₹{self.amount} for {self.invoice.invoice_no}"
