from django.urls import path
from .views import success, cancel

urlpatterns = [
    path("cancel/", cancel, name="cancel"),
    path("success/", success, name="success"),
]
