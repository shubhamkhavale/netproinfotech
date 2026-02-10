from django.contrib import admin
from .models import Vendor

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'phone', 'gst_number')
    search_fields = ('name', 'company_name', 'phone')
