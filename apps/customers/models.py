from django.db import models
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from django.db.models import Sum, Max
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)
    
    def business_customers(self):
        return self.filter(customer_type__in=['business', 'government', 'dealer', 'reseller'])
    
    def individual_customers(self):
        return self.filter(customer_type='individual')
    
    def with_outstanding_balance(self):
        return self.filter(outstanding_balance__gt=0)

class CustomerManager(models.Manager):
    def get_queryset(self):
        return CustomerQuerySet(self.model, using=self._db)
    
    def active(self):
        return self.get_queryset().active()
    
    def business_customers(self):
        return self.get_queryset().business_customers()
    
    def individual_customers(self):
        return self.get_queryset().individual_customers()
    
    def with_outstanding_balance(self):
        return self.get_queryset().with_outstanding_balance()


class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('government', 'Government'),
        ('dealer', 'Dealer'),
        ('reseller', 'Reseller'),
    ]
    
    BUSINESS_TYPE_CHOICES = [
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('service', 'Service'),
        ('manufacturing', 'Manufacturing'),
        ('other', 'Other'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online Transfer'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, verbose_name="Customer Name")
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Company Name")
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual', verbose_name="Customer Type")
    customer_category = models.CharField(max_length=50, blank=True, null=True, verbose_name="Category")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    # Contact Information
    phone = models.CharField(
        max_length=15, 
        verbose_name="Phone Number",
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    mobile = models.CharField(max_length=15, blank=True, null=True, verbose_name="Mobile Number")
    email = models.EmailField(
        verbose_name="Email Address",
        validators=[EmailValidator()],
        blank=True,
        null=True
    )
    secondary_email = models.EmailField(blank=True, null=True, verbose_name="Secondary Email")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    
    # Address Information
    address = models.TextField(verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    district = models.CharField(max_length=100, verbose_name="District")
    state = models.CharField(max_length=100, default="Maharashtra", verbose_name="State")
    pincode = models.CharField(max_length=10, blank=True, null=True, verbose_name="PIN Code")
    country = models.CharField(max_length=100, default="India", verbose_name="Country")
    
    # Business/Tax Information
    gst_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="GST Number")
    pan_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="PAN Number")
    registration_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Registration Number")
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES, blank=True, null=True, verbose_name="Business Type")
    
    # Financial Information
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Credit Limit")
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Outstanding Balance")
    total_amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Total Amount Paid")
    preferred_payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', verbose_name="Preferred Payment Method")
    payment_terms = models.CharField(max_length=200, blank=True, null=True, verbose_name="Payment Terms")
    
    # Additional Information
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='customers', verbose_name="Assigned To")
    
    # Statistics (automatically updated)
    total_purchases = models.IntegerField(default=0, verbose_name="Total Purchases")
    last_purchase_date = models.DateTimeField(blank=True, null=True, verbose_name="Last Purchase Date")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_customers', verbose_name="Created By")
    
    objects = CustomerManager()
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['city']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        if self.company_name:
            return f"{self.name} - {self.company_name}"
        return self.name
    
    def save(self, *args, **kwargs):
        # Save the instance first
        super().save(*args, **kwargs)
        
        # Then auto-calculate statistics
        from apps.invoices.models import Invoice
        from apps.payments.models import Payment
        
        # Calculate total purchases from invoices
        invoices = Invoice.objects.filter(customer=self)
        self.total_purchases = invoices.count()
        if invoices.exists():
            self.last_purchase_date = invoices.latest('created_at').created_at
        
        # Calculate total amount paid from payments
        payments = Payment.objects.filter(invoice__customer=self)
        total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        self.total_amount_paid = total_paid
        
        # Calculate outstanding balance
        total_invoice_amount = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        self.outstanding_balance = total_invoice_amount - total_paid
        
        # Only update if stats actually changed
        if self.total_purchases > 0 or total_paid > 0:
            super().save(update_fields=[
                'total_purchases', 
                'last_purchase_date', 
                'total_amount_paid', 
                'outstanding_balance'
            ])
    
    def get_full_address(self):
        """Returns formatted address"""
        address_parts = [
            self.address,
            f"{self.city} - {self.district}",
            f"{self.state} - {self.pincode}" if self.pincode else self.state,
            self.country
        ]
        return ", ".join(filter(None, address_parts))
    
    def get_contact_info(self):
        """Returns formatted contact information"""
        contacts = []
        if self.phone:
            contacts.append(f"Phone: {self.phone}")
        if self.mobile:
            contacts.append(f"Mobile: {self.mobile}")
        if self.email:
            contacts.append(f"Email: {self.email}")
        if self.website:
            contacts.append(f"Website: {self.website}")
        return "\n".join(contacts)
    
    @property
    def is_business_customer(self):
        return self.customer_type in ['business', 'government', 'dealer', 'reseller']
    
    @property
    def has_gst(self):
        return bool(self.gst_number)
    
    @property
    def total_spent(self):
        """Total amount spent by customer"""
        from apps.invoices.models import Invoice
        total = Invoice.objects.filter(
            customer=self, 
            status='paid'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        return total
    
    @property
    def pending_invoices(self):
        """Get pending invoices count"""
        from apps.invoices.models import Invoice
        return Invoice.objects.filter(
            customer=self,
            status__in=['sent', 'overdue']
        ).count()
    
    def update_statistics(self):
        """Update customer statistics"""
        from apps.invoices.models import Invoice
        from apps.payments.models import Payment
        
        invoices = Invoice.objects.filter(customer=self)
        payments = Payment.objects.filter(customer=self)
        
        self.total_purchases = invoices.count()
        if invoices.exists():
            self.last_purchase_date = invoices.latest('created_at').created_at
        
        total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        self.total_amount_paid = total_paid
        
        total_invoice_amount = invoices.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        self.outstanding_balance = total_invoice_amount - total_paid
        
        self.save(update_fields=[
            'total_purchases', 
            'last_purchase_date', 
            'total_amount_paid', 
            'outstanding_balance'
        ])

# QuerySet Manager
