from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout_page, name='checkout_page'),
    path('api/product/<int:product_id>/', views.get_product, name='get_product'),
    path('api/complete_order/', views.complete_order, name='complete_order'),
]