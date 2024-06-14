import stripe
from django.conf import settings
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from products.models import Product
stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs["pk"]
        product = Product.objects.get(id=product_id)
        YOUR_DOMAIN = "https://127.0.0.1:8000/"
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': product.price,
                            'product_data': {
                                "name": product.name,
                            }
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
        except Exception as e:
            return str(e)

        return JsonResponse({
            'id': checkout_session.id
        })

def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")