from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Receipt

def receipt_list(request):
    receipts = Receipt.objects.all().order_by('-created_at') if hasattr(Receipt, 'created_at') else Receipt.objects.all()
    return render(request, 'receipts/list.html', {'receipts': receipts})


def receipt_pdf(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    template = get_template('receipts/receipt_pdf.html')
    html = template.render({'receipt': receipt})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{receipt.receipt_no}.pdf"'

    pisa.CreatePDF(html, dest=response)
    return response
