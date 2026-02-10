from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentForm
from .models import Payment
from apps.invoices.models import Invoice
from apps.receipts.models import Receipt
import uuid

def add_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice = invoice
            payment.save()

            # ✅ Create receipt after payment is saved
            Receipt.objects.create(
                receipt_no=f"RCPT-{uuid.uuid4().hex[:6].upper()}",
                invoice=invoice,
                payment=payment
            )

            # ✅ Update invoice status
            total_paid = sum(p.amount for p in invoice.payments.all())
            if total_paid >= invoice.total_amount:
                invoice.status = 'PAID'
            else:
                invoice.status = 'PARTIAL'
            invoice.save()

            return redirect('invoices:detail', pk=invoice.id)
    else:
        # prefill amount with outstanding balance
        total_paid = sum(p.amount for p in invoice.payments.all())
        outstanding = float(invoice.total_amount) - float(total_paid)
        form = PaymentForm(initial={'amount': outstanding if outstanding > 0 else 0})

    # ensure form widgets have bootstrap classes for both GET and POST flows
    try:
        form.fields['amount'].widget.attrs.update({'class': 'form-control form-control-lg', 'step': '0.01'})
        form.fields['payment_mode'].widget.attrs.update({'class': 'form-select'})
        form.fields['transaction_id'].widget.attrs.update({'class': 'form-control'})
        form.fields['remarks'].widget.attrs.update({'class': 'form-control', 'rows': '3'})
    except Exception:
        pass

    # compute totals for template
    total_paid = sum(p.amount for p in invoice.payments.all())
    outstanding = float(invoice.total_amount) - float(total_paid)

    return render(request, 'payments/add_payment.html', {
        'invoice': invoice,
        'form': form,
        'total_paid': total_paid,
        'outstanding': outstanding,
    })


def payment_list(request):
    payments = Payment.objects.select_related('invoice').all().order_by('-payment_date')
    return render(request, 'payments/list.html', {'payments': payments})
