from collections import Counter
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, OrderItem
import json

def checkout_page(request):
    return render(request, 'products/checkout.html')

def get_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        'id': product.id,
        'name': product.name,
        'price': str(product.price),
        'stock': product.stock,
    }
    return JsonResponse(data)

@csrf_exempt
def complete_order(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    body = json.loads(request.body)
    product_ids = body.get('product_ids', [])
    counts = Counter(product_ids)

    with transaction.atomic():
        products = {p.id: p for p in Product.objects.filter(id__in=counts.keys())}

        for pid, qty in counts.items():
            product = products.get(pid)
            if product is None:
                return JsonResponse({'error': 'Product not found'}, status=404)
            if product.stock < qty:
                return JsonResponse(
                    {'error': f'Only {product.stock} left in stock for {product.name}'},
                    status=400
                )

        order = Order.objects.create(total_amount=0)
        total = 0

        for pid, qty in counts.items():
            product = products[pid]
            for _ in range(qty):
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price_at_purchase=product.price
                )
                total += product.price
            product.stock -= qty
            product.save(update_fields=['stock'])

        order.total_amount = total
        order.save()

    return JsonResponse({'order_id': order.id, 'total': str(total)})

def receipt_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Group the same product into one line with quantity
    lines = {}
    for item in order.items.select_related('product'):
        key = (item.product_id, item.price_at_purchase)
        if key not in lines:
            lines[key] = {
                'name': item.product.name,
                'price': item.price_at_purchase,
                'qty': 0,
                'subtotal': 0,
            }
        lines[key]['qty'] += 1
        lines[key]['subtotal'] += item.price_at_purchase

    return render(request, 'products/receipt.html', {
        'order': order,
        'lines': list(lines.values()),
    })