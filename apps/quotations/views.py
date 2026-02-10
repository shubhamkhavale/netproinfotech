from django.shortcuts import render, redirect, get_object_or_404
from .models import Quotation, QuotationItem
from apps.customers.models import Customer
from apps.products.models import Product
from .services import calculate_quotation_total
from django.utils.timezone import now


def quotation_list(request):
    quotations = Quotation.objects.all().order_by('-created_at') if hasattr(Quotation, 'created_at') else Quotation.objects.all()
    return render(request, 'quotations/list.html', {'quotations': quotations})

def create_quotation(request):
    customers = Customer.objects.all()
    products = Product.objects.filter(is_active=True)

    if request.method == "POST":
        customer_id = request.POST.get('customer')
        
        # Validate customer selection
        if not customer_id:
            return render(request, 'quotations/create.html', {
                'customers': customers,
                'products': products,
                'error': 'Please select a customer'
            })
        
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return render(request, 'quotations/create.html', {
                'customers': customers,
                'products': products,
                'error': 'Selected customer does not exist'
            })

        quotation_no = f"QT-{now().strftime('%Y%m%d%H%M%S')}"
        quotation = Quotation.objects.create(
            quotation_no=quotation_no,
            customer=customer
        )

        items = []
        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')

        for i in range(len(product_ids)):
            product = Product.objects.get(id=product_ids[i])
            qty = int(quantities[i])
            price = product.price
            total = price * qty

            item = QuotationItem.objects.create(
                quotation=quotation,
                product=product,
                quantity=qty,
                price=price,
                total=total
            )
            items.append(item)

        quotation.total_amount = calculate_quotation_total(items)
        quotation.save()

        return redirect('quotations:detail', pk=quotation.id)

    return render(request, 'quotations/create.html', {
        'customers': customers,
        'products': products
    })


def quotation_detail(request, pk):
    quotation = get_object_or_404(Quotation, pk=pk)
    return render(request, 'quotations/detail.html', {'quotation': quotation})
