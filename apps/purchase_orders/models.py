from django.db import models

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor_name = models.CharField(max_length=200)
    order_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('received', 'Received'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    def __str__(self):
        return self.po_number
