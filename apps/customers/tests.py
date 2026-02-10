import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netproinfotech.settings')
django.setup()

from apps.customers.models import Customer
print(f"Total customers: {Customer.objects.count()}")
for customer in Customer.objects.all()[:5]:
    print(f"- {customer.name} ({customer.phone})")