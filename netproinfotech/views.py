from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum

def home(request):
    """Home/Landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'home.html')

@login_required
def dashboard(request):
    """Main dashboard for authenticated users"""
    context = {
        'title': 'Dashboard - NETPRO INFOTECH',
        'page_name': 'Dashboard'
    }
    return render(request, 'dashboard.html', context)


@login_required
def dashboard_summary(request):
    """Return small business summary as JSON for real-time dashboard updates."""
    try:
        from apps.customers.models import Customer
        from apps.products.models import Product
        from apps.quotations.models import Quotation
        from apps.invoices.models import Invoice
    except Exception:
        return JsonResponse({'error': 'models not available'}, status=500)

    total_customers = Customer.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    pending_quotations = Quotation.objects.filter(invoice__isnull=True).count()
    unpaid_invoices = Invoice.objects.filter(status='UNPAID').count()
    total_sales = Invoice.objects.filter(status='PAID').aggregate(total=Sum('total_amount'))['total'] or 0
    outstanding_amount = Invoice.objects.exclude(status='PAID').aggregate(total=Sum('total_amount'))['total'] or 0

    data = {
        'total_customers': total_customers,
        'active_products': active_products,
        'pending_quotations': pending_quotations,
        'unpaid_invoices': unpaid_invoices,
        'total_sales': float(total_sales),
        'outstanding_amount': float(outstanding_amount),
    }
    return JsonResponse(data)


@login_required
def recent_invoices_json(request):
    """Return last 10 invoices as JSON for realtime dashboard list."""
    try:
        from apps.invoices.models import Invoice
    except Exception:
        return JsonResponse({'error': 'invoices model not available'}, status=500)

    invoices = Invoice.objects.order_by('-date')[:10]
    items = []
    for inv in invoices:
        items.append({
            'invoice_no': inv.invoice_no,
            'customer': inv.customer.name if inv.customer else '',
            'date': inv.date.isoformat(),
            'amount': float(inv.total_amount),
            'status': inv.status,
        })
    return JsonResponse({'invoices': items})


@login_required
def sales_overview_json(request):
    """Return aggregated sales per day for last N days for charting."""
    try:
        from apps.invoices.models import Invoice
    except Exception:
        return JsonResponse({'error': 'invoices model not available'}, status=500)

    from datetime import date, timedelta
    days = int(request.GET.get('days', 30))
    start = date.today() - timedelta(days=days - 1)

    qs = (
        Invoice.objects.filter(date__gte=start, status='PAID')
        .values('date')
        .annotate(total=Sum('total_amount'))
        .order_by('date')
    )

    # build full series with zeros for missing dates
    series = {}
    for row in qs:
        series[row['date'].isoformat()] = float(row['total'] or 0)

    labels = []
    data = []
    for i in range(days):
        d = start + timedelta(days=i)
        iso = d.isoformat()
        labels.append(iso)
        data.append(series.get(iso, 0.0))

    return JsonResponse({'labels': labels, 'data': data})


@login_required
def top_products_json(request):
    """Return top selling products for the current month as JSON."""
    try:
        from apps.invoices.models import InvoiceItem
        from apps.products.models import Product
        from django.db.models import Sum
        from datetime import date
    except Exception:
        return JsonResponse({'error': 'models not available'}, status=500)

    today = date.today()
    start_month = today.replace(day=1)

    qs = (
        InvoiceItem.objects.filter(invoice__date__gte=start_month, invoice__status='PAID')
        .values('product')
        .annotate(sold=Sum('quantity'))
        .order_by('-sold')[:5]
    )

    items = []
    product_map = {p.id: p.name for p in Product.objects.filter(id__in=[r['product'] for r in qs])}
    for row in qs:
        pid = row['product']
        items.append({'product_id': pid, 'name': product_map.get(pid, 'Unknown'), 'sold': int(row['sold'] or 0)})

    return JsonResponse({'top_products': items})

def about(request):
    """About page"""
    return render(request, 'about.html', {'title': 'About Us - NETPRO INFOTECH'})

def contact(request):
    """Contact page"""
    return render(request, 'contact.html', {'title': 'Contact - NETPRO INFOTECH'})