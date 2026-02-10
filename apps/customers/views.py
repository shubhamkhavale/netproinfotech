from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def customer_list(request):
    """Customer list view"""
    customers = Customer.objects.all().order_by('-id')
    
    context = {
        'customers': customers,
        'title': 'Customers',
        'total': customers.count()
    }
    return render(request, 'customers/list.html', context)

@login_required
def customer_create(request):
    """Simple customer create view for testing"""
    if request.method == 'POST':
        # Simple creation logic
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        
        customer = Customer.objects.create(
            name=name,
            phone=phone,
            address=address,
            city=city,
            state=request.POST.get('state', 'Maharashtra'),
            email=request.POST.get('email'),
            company_name=request.POST.get('company_name'),
            customer_type=request.POST.get('customer_type', 'individual'),
            gst_number=request.POST.get('gst_number'),
            created_by=request.user
        )
        return redirect('customers:detail', customer_id=customer.id)
    
    return render(request, 'customers/create.html', {'title': 'Add Customer'})

@login_required
def customer_detail(request, customer_id):
    """Simple customer detail view for testing"""
    from django.shortcuts import get_object_or_404
    customer = get_object_or_404(Customer, id=customer_id)
    
    context = {
        'customer': customer,
        'title': f'{customer.name} - Details'
    }
    return render(request, 'customers/detail.html', context)

# Add other simple views
def customer_edit(request, customer_id):
    from django.shortcuts import get_object_or_404
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name', customer.name)
        customer.phone = request.POST.get('phone', customer.phone)
        customer.address = request.POST.get('address', customer.address)
        customer.city = request.POST.get('city', customer.city)
        customer.email = request.POST.get('email', customer.email)
        customer.company_name = request.POST.get('company_name', customer.company_name)
        customer.save()
        return redirect('customers:detail', customer_id=customer.id)
    
    return render(request, 'customers/edit.html', {'customer': customer})

def customer_delete(request, customer_id):
    from django.shortcuts import get_object_or_404
    customer = get_object_or_404(Customer, id=customer_id)
    customer.delete()
    return redirect('customers:list')