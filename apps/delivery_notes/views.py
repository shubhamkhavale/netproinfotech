from django.shortcuts import render
from .models import DeliveryNote

def delivery_note_list(request):
    notes = DeliveryNote.objects.all()
    return render(request, 'delivery_notes/list.html', {'notes': notes})
