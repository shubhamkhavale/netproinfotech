from django.db import models

class DeliveryNote(models.Model):
    delivery_no = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=200)
    delivery_date = models.DateField(auto_now_add=True)
    reference_invoice = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('delivered', 'Delivered'),
        ],
        default='pending'
    )
    remarks = models.TextField(blank=True)

    def __str__(self):
        return self.delivery_no
