from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    @property
    def get_url(self):
        return reverse("product_detail", kwargs={
            "pk": self.pk
        })
