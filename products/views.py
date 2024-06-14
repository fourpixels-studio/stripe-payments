from django.shortcuts import render, get_object_or_404
from .models import Product
from django.conf import settings
import stripe
from django.views import View
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


def product_list(request):
    context = {}

    context.update({
        "title_tag": "All products",
        "products": Product.objects.order_by("-pk"),
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    })
    return render(request, "product_list.html", context)


def product_detail(request, pk):
    context = {}
    product = get_object_or_404(Product, pk=pk)

    context.update({
        "title_tag": product.name,
        "product": product,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY,
    })
    return render(request, "product_detail.html", context)
