import stripe
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse
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
                metadata={
                    'product_id': product.id,
                },
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
        except Exception as e:
            return str(e)

        return JsonResponse({
            'id': checkout_session.id
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature_header,
            # endpoint_secret
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # that means that the actual data in the payload is invalid
        # returns the status 400
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # verification of the signature fails, return the code 400
        return HttpResponse(status=400)

    # handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # fullfill the purchase
        customer_email = session['customer_details']['email']
        product_id = session['metadata']['product_id']

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email,],
            from_email="no-reply@stripe-payments.com",
        )

    elif event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']

        stripe_customer_id = intent['customer']
        stripe_customer = stripe.Customer.retrieve(stripe_customer_id)

        customer_email = stripe_customer['email']
        product_id = intent['metadata']['product_id']

        product = Product.objects.get(id=product_id)

        send_mail(
            subject="Here is your product",
            message=f"Thanks for your purchase. Here is the product you ordered. The URL is {product.url}",
            recipient_list=[customer_email,],
            from_email="no-reply@stripe-payments.com",
        )

    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            request_json = json.loads(request.body)
            customer = stripe.Customer.create(email=request_json['email'])
            product_id = self.kwargs['pk']
            product = Product.objects.get(id=product_id)
            intent = stripe.PaymentIntent.create(
                amount=product.price,
                currency='usd',
                customer=customer['id'],
                metadata={
                    'product_id': product.id
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
