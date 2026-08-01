from django.db import models
from io import BytesIO
from django.core.files import File
import qrcode

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.qr_code:
            qr_data = str(self.id)
            qr_img = qrcode.make(qr_data)

            buffer = BytesIO()
            qr_img.save(buffer, format='PNG')
            filename = f'product_{self.id}.png'

            self.qr_code.save(filename, File(buffer), save=False)
            super().save(update_fields=['qr_code'])


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - ₹{self.total_amount}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - ₹{self.price_at_purchase}"