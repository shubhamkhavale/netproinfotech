from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Invoice
from apps.business.models import Business


def render_to_pdf(template_src, context):
    template = get_template(template_src)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response)
    return response


def invoice_pdf(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    business = Business.objects.first()

    context = {
        'invoice': invoice,
        'business': business
    }

    return render_to_pdf('pdf/invoice_pdf.html', context)
