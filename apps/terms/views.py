from django.shortcuts import render
from .models import Term

def term_list(request):
    terms = Term.objects.filter(is_active=True)
    return render(request, 'terms/list.html', {'terms': terms})
