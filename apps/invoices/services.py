from django.utils.timezone import now
from .models import Invoice, InvoiceItem
# from apps.invoices.models import Invoice


def create_invoice_from_quotation(quotation):
    invoice = Invoice.objects.create(
        invoice_no=f"INV-{now().strftime('%Y%m%d%H%M%S')}",
        quotation=quotation,
        customer=quotation.customer,
        total_amount=quotation.total_amount
    )

    for item in quotation.items.all():
        InvoiceItem.objects.create(
            invoice=invoice,
            product=item.product,
            quantity=item.quantity,
            price=item.price,
            total=item.total
        )

    return invoice
