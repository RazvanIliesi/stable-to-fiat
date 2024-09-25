from django.db import models


# Create your models here.

class Offer(models.Model):
    active_option = [
        (True, "Online"),
        (False, "Offline"),
    ]

    name = models.CharField(max_length=100)
    logo = models.ImageField()
    abbreviation = models.CharField(max_length=10)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(choices=active_option)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.abbreviation}"

