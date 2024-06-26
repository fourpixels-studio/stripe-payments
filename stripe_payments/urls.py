"""
URL configuration for stripe_payments project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from backend.views import CreateCheckoutSessionView, stripe_webhook, StripeIntentView, success, cancel

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("frontend.urls")),
    path("backend/", include("backend.urls")),
    path("products/", include("products.urls")),
    path("create-checkout-session/<int:pk>/", CreateCheckoutSessionView.as_view(), name="create_checkout_session"),
    path("create-payment-intent/<int:pk>/", StripeIntentView.as_view(), name="create_payment_intent"),
    path("stripe-webhook", stripe_webhook, name="stripe_webhook"),
    path("cancel/", cancel, name="cancel"),
    path("success/", success, name="success"),
]
