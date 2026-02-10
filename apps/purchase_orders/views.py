from django.shortcuts import render
from .models import PurchaseOrder

def purchase_order_list(request):
    orders = PurchaseOrder.objects.all()
    return render(request, 'purchase_orders/list.html', {'orders': orders})
