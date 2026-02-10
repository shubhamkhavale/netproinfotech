from django import forms
from .models import BusinessProfile

class BusinessProfileForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            'name', 'tagline', 'logo', 'address', 'city', 'district',
            'state', 'pincode', 'phone', 'mobile', 'email', 'website',
            'gst_number', 'pan_number', 'registration_number',
            'bank_name', 'account_number', 'account_holder', 'ifsc_code', 'branch',
            'facebook', 'twitter', 'instagram', 'linkedin'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter business name'
            }),
            'tagline': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter tagline or slogan'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter full address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city'
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter district'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter state'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PIN code'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter website URL'
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter GST number'
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PAN number'
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter bank name'
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter account number'
            }),
            'ifsc_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter IFSC code'
            }),
            'branch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter branch name'
            }),
            'footer_note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter footer note for documents'
            }),
            'terms_and_conditions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter terms and conditions'
            }),
            'payment_terms': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter payment terms'
            }),
        }

class BusinessSettingsForm(forms.ModelForm):
    class Meta:
        model = BusinessProfile
        fields = [
            'invoice_prefix', 'quotation_prefix', 'receipt_prefix',
            'proforma_prefix', 'purchase_order_prefix',
            'invoice_start_number', 'quotation_start_number',
            'currency', 'currency_name', 'tax_rate',
            'opening_time', 'closing_time', 'working_days',
            'footer_note', 'terms_and_conditions', 'payment_terms'
        ]
        widgets = {
            'invoice_prefix': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., INV, NETPRO-INV'
            }),
            'quotation_prefix': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., QUO, NETPRO-QUO'
            }),
            'receipt_prefix': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., REC, NETPRO-REC'
            }),
            'invoice_start_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'quotation_start_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'tax_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'opening_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'closing_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'working_days': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Monday to Saturday'
            }),
        }