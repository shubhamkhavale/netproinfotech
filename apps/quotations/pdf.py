from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Quotation
from apps.business.models import Business


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa.CreatePDF(html, dest=response)
    return response


def quotation_pdf(request, pk):
    quotation = Quotation.objects.get(pk=pk)
    business = Business.objects.first()

    context = {
        'quotation': quotation,
        'business': business
    }

    return render_to_pdf('pdf/quotation_pdf.html', context)
