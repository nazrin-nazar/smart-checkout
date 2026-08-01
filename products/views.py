from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
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
    }
    return JsonResponse(data)

@csrf_exempt
def complete_order(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        product_ids = body.get('product_ids', [])

        order = Order.objects.create(total_amount=0)
        total = 0

        for pid in product_ids:
            product = get_object_or_404(Product, id=pid)
            OrderItem.objects.create(
                order=order,
                product=product,
                price_at_purchase=product.price
            )
            total += product.price

        order.total_amount = total
        order.save()

        return JsonResponse({'order_id': order.id, 'total': str(total)})