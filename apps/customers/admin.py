from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'phone', 'email', 'customer_type', 
                    'total_purchases', 'last_purchase_date', 'is_active')
    list_filter = ('customer_type', 'is_active', 'city', 'state', 'created_at')
    search_fields = ('name', 'company_name', 'phone', 'email', 'gst_number', 'pan_number')
    list_editable = ('is_active',)
    readonly_fields = ('total_purchases', 'last_purchase_date', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'company_name', 'customer_type', 'customer_category', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone', 'mobile', 'email', 'website', 'secondary_email')
        }),
        ('Address', {
            'fields': ('address', 'city', 'district', 'state', 'pincode', 'country')
        }),
        ('Business Details', {
            'fields': ('gst_number', 'pan_number', 'registration_number', 'business_type')
        }),
        ('Additional Information', {
            'fields': ('notes', 'preferred_payment_method', 'credit_limit', 'payment_terms')
        }),
        ('Statistics', {
            'fields': ('total_purchases', 'last_purchase_date', 'total_amount_paid')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate_purchase_stats()
        return queryset
    
    def total_purchases(self, obj):
        return obj.total_purchases or 0
    total_purchases.short_description = 'Total Orders'
    total_purchases.admin_order_field = 'total_purchases'
    
    def last_purchase_date(self, obj):
        return obj.last_purchase_date or 'Never'
    last_purchase_date.short_description = 'Last Purchase'
    last_purchase_date.admin_order_field = 'last_purchase_date'
    
    actions = ['activate_customers', 'deactivate_customers', 'export_customers']
    
    def activate_customers(self, request, queryset):
        updated = queryset.update(is_active=True, updated_at=timezone.now())
        self.message_user(request, f'{updated} customers activated successfully.')
    activate_customers.short_description = "Activate selected customers"
    
    def deactivate_customers(self, request, queryset):
        updated = queryset.update(is_active=False, updated_at=timezone.now())
        self.message_user(request, f'{updated} customers deactivated successfully.')
    deactivate_customers.short_description = "Deactivate selected customers"