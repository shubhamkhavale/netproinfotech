"""
URL configuration for netproinfotech project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # Temporary helper: provide a top-level `create` name to avoid NoReverseMatch
    # when some templates or code call `reverse('create')` without a namespace.
    path('create/', views.home, name='create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/summary/', views.dashboard_summary, name='dashboard-summary'),
    path('dashboard/recent-invoices/', views.recent_invoices_json, name='dashboard-recent-invoices'),
    path('dashboard/sales-overview/', views.sales_overview_json, name='dashboard-sales-overview'),
    path('dashboard/top-products/', views.top_products_json, name='dashboard-top-products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    path('admin/', admin.site.urls),
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),
    path('customers/', include(('apps.customers.urls', 'customers'), namespace='customers')),
    path('business/', include(('apps.business.urls', 'business'), namespace='business')),
    path('products/', include(('apps.products.urls', 'products'), namespace='products')),
    path('invoices/', include(('apps.invoices.urls', 'invoices'), namespace='invoices')),
    path('payments/', include(('apps.payments.urls', 'payments'), namespace='payments')),
    path('quotations/', include(('apps.quotations.urls', 'quotations'), namespace='quotations')),
    path('delivery-notes/', include(('apps.delivery_notes.urls', 'delivery_notes'), namespace='delivery_notes')),
    path('receipts/', include(('apps.receipts.urls', 'receipts'), namespace='receipts')),
    path('reports/', include(('apps.reports.urls', 'reports'), namespace='reports')),
    path('terms/', include(('apps.terms.urls', 'terms'), namespace='terms')),
    path('vendors/', include(('apps.vendors.urls', 'vendors'), namespace='vendors')),
    path('purchase-orders/', include(('apps.purchase_orders.urls', 'purchase_orders'), namespace='purchase_orders')),
    path('proforma/', include(('apps.proforma.urls', 'proforma'), namespace='proforma')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
