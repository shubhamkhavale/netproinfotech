from django.shortcuts import render, redirect, get_object_or_404
from .models import Invoice
from .services import create_invoice_from_quotation
from apps.quotations.models import Quotation

def create_invoice(request, quotation_id=None):
    # Allow creating an invoice by passing a quotation id either via URL
    # (existing behavior) or via GET parameter (e.g. ?quotation=123).
    if quotation_id is None:
        qid = request.GET.get('quotation') or request.GET.get('quotation_id')
        if qid:
            try:
                quotation_id = int(qid)
            except (TypeError, ValueError):
                quotation_id = None

    if quotation_id is None:
        # No quotation provided — redirect to invoice list for now.
        return redirect('invoices:list')

    quotation = get_object_or_404(Quotation, id=quotation_id)
    invoice = create_invoice_from_quotation(quotation)
    return redirect('invoices:detail', pk=invoice.id)

def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoices/detail.html', {'invoice': invoice})


def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'invoices/list.html', {'invoices': invoices})
