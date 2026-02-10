from django.shortcuts import render
from .models import Vendor

def vendor_list(request):
    vendors = Vendor.objects.all()
    return render(request, 'vendors/list.html', {'vendors': vendors})
