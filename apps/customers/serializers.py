from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer

User = get_user_model()

class CustomerSerializer(serializers.ModelSerializer):
    full_address = serializers.SerializerMethodField()
    contact_info = serializers.SerializerMethodField()
    is_business_customer = serializers.BooleanField(read_only=True)
    has_gst = serializers.BooleanField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    pending_invoices = serializers.IntegerField(read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'total_purchases', 
                           'last_purchase_date', 'total_amount_paid', 'outstanding_balance')
    
    def get_full_address(self, obj):
        return obj.get_full_address()
    
    def get_contact_info(self, obj):
        return obj.get_contact_info()
    
    def validate_phone(self, value):
        import re
        if not re.match(r'^\+?1?\d{9,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number.")
        return value
    
    def validate_email(self, value):
        if value:
            from django.core.validators import validate_email
            try:
                validate_email(value)
            except:
                raise serializers.ValidationError("Enter a valid email address.")
        return value
    
    def validate_gst_number(self, value):
        if value:
            import re
            # Basic GST validation (15 characters, alphanumeric)
            if not re.match(r'^[0-9A-Z]{15}$', value):
                raise serializers.ValidationError("Enter a valid 15-character GST number.")
        return value
    
    def create(self, validated_data):
        # Set created_by to current user
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['created_by'] = request.user
        return super().create(validated_data)

class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'company_name', 'phone', 'email', 
                 'city', 'customer_type', 'is_active', 'total_purchases',
                 'outstanding_balance')

class CustomerMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'name', 'company_name', 'phone', 'email')

class CustomerImportSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    def validate_file(self, value):
        import os
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.xlsx', '.xls', '.csv']
        if not ext.lower() in valid_extensions:
            raise serializers.ValidationError('Unsupported file type. Please upload Excel or CSV file.')
        return value

class CustomerExportSerializer(serializers.Serializer):
    fields = serializers.ListField(
        child=serializers.CharField(),
        default=['name', 'company_name', 'phone', 'email', 'address', 'city']
    )
    format = serializers.ChoiceField(choices=['csv', 'excel', 'pdf'], default='excel')