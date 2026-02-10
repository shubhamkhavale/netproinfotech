from datetime import date
from apps.purchase_orders.models import PurchaseOrder
from apps.payments.models import Payment
from apps.invoices.models import Invoice

def sales_report(start_date=None, end_date=None):
    qs = Invoice.objects.all()

    if start_date:
        qs = qs.filter(date__gte=start_date)
    if end_date:
        qs = qs.filter(date__lte=end_date)

    total_sales = sum(inv.total_amount for inv in qs)

    return {
        "count": qs.count(),
        "total_sales": total_sales,
        "invoices": list(qs),
        "average_sale": total_sales / qs.count() if qs.count() > 0 else 0
    }


def purchase_report(start_date=None, end_date=None):
    qs = PurchaseOrder.objects.all()

    if start_date:
        qs = qs.filter(order_date__gte=start_date)
    if end_date:
        qs = qs.filter(order_date__lte=end_date)

    total_purchase = sum(po.total_amount for po in qs)

    return {
        "count": qs.count(),
        "total_purchase": total_purchase,
        "purchase_orders": list(qs),
        "average_purchase": total_purchase / qs.count() if qs.count() > 0 else 0
    }


def outstanding_payments():
    invoices = Invoice.objects.filter(status__in=['UNPAID', 'PARTIAL'])
    total_due = 0
    
    for inv in invoices:
        paid_amount = sum(p.amount for p in inv.payments.all())
        outstanding = inv.total_amount - paid_amount
        total_due += outstanding

    return {
        "pending_invoices": list(invoices),
        "total_due": total_due,
        "invoice_count": invoices.count()
    }
