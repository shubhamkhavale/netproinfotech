from decimal import Decimal

def calculate_quotation_total(items):
    total = Decimal('0.00')
    for item in items:
        total += item.total
    return total
