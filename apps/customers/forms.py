from django import forms
from django.core.validators import EmailValidator, RegexValidator
from .models import Customer

class CustomerForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number',
            'required': 'required'
        })
    )
    
    email = forms.EmailField(
        required=False,
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address'
        })
    )
    
    class Meta:
        model = Customer
        fields = [
            'name', 'company_name', 'customer_type', 'customer_category',
            'phone', 'mobile', 'email', 'secondary_email', 'website',
            'address', 'city', 'district', 'state', 'pincode', 'country',
            'gst_number', 'pan_number', 'registration_number', 'business_type',
            'credit_limit', 'preferred_payment_method', 'payment_terms',
            'notes', 'assigned_to', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter customer name',
                'required': 'required'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),
            'customer_type': forms.Select(attrs={'class': 'form-select'}),
            'customer_category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category (e.g., VIP, Regular)'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter mobile number'
            }),
            'secondary_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter secondary email'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter website URL'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter complete address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter city',
                'required': 'required'
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
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter country'
            }),
            'gst_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter GST number'
            }),
            'pan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter PAN number'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter registration number'
            }),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'credit_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'preferred_payment_method': forms.Select(attrs={'class': 'form-select'}),
            'payment_terms': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Net 30, Due on receipt'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter any notes or remarks'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = self.fields['assigned_to'].queryset.filter(is_active=True)
    
    def clean_gst_number(self):
        gst_number = self.cleaned_data.get('gst_number')
        if gst_number:
            import re
            if not re.match(r'^[0-9A-Z]{15}$', gst_number):
                raise forms.ValidationError("Enter a valid 15-character GST number.")
        return gst_number
    
    def clean_pan_number(self):
        pan_number = self.cleaned_data.get('pan_number')
        if pan_number:
            import re
            if not re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', pan_number):
                raise forms.ValidationError("Enter a valid PAN number (e.g., ABCDE1234F).")
        return pan_number

class CustomerImportForm(forms.Form):
    file = forms.FileField(
        label='Select file',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv,.xlsx,.xls'
        })
    )
    
    def clean_file(self):
        file = self.cleaned_data['file']
        import os
        ext = os.path.splitext(file.name)[1]
        valid_extensions = ['.xlsx', '.xls', '.csv']
        if not ext.lower() in valid_extensions:
            raise forms.ValidationError('Unsupported file type. Please upload Excel or CSV file.')
        return file

class CustomerSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search customers...'
        })
    )
    customer_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Customer.CUSTOMER_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by city'
        })
    )
    active = forms.ChoiceField(
        required=False,
        choices=[('', 'All'), ('true', 'Active'), ('false', 'Inactive')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )