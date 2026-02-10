from django.shortcuts import render
from .models import ProformaInvoice

def proforma_list(request):
    proformas = ProformaInvoice.objects.all()
    return render(request, 'proforma/list.html', {'proformas': proformas})
