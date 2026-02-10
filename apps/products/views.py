from django.shortcuts import render, redirect
from .models import Product, ProductCategory


def product_list(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.filter(is_active=True)
    return render(
        request,
        'products/list.html',
        {
            'categories': categories,
            'products': products
        }
    )


def product_create(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price') or 0
        stock = request.POST.get('stock') or 0
        is_active = 'is_active' in request.POST
        
        Product.objects.create(
            category_id=category_id,
            name=name,
            description=description,
            price=price,
            stock=stock,
            is_active=is_active
        )
        return redirect('products:list')
    categories = ProductCategory.objects.all()
    return render(request, 'products/create.html', {'categories': categories})
