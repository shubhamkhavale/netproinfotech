from django.db import models

class ProformaInvoice(models.Model):
    proforma_no = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    valid_till = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('converted', 'Converted to Invoice'),
        ],
        default='draft'
    )

    def __str__(self):
        return self.proforma_no
