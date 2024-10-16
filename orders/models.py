import uuid

from django.db import models

from offers.models import Offer
from users.models import UserKYC


class Order(models.Model):
    type_option = [
        ("sell", "Buy"),
        ("buy", "Sell"),
    ]
    status_option = [
        ("complete", "Complete"),
        ("pending", "Pending"),
        ("canceled", "Canceled"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_kyc = models.ForeignKey(UserKYC, on_delete=models.CASCADE, related_name='orders')
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='orders')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    order_type = models.CharField(max_length=10, choices=type_option)
    status = models.CharField(max_length=10, choices=status_option, default="pending")

    def __str__(self):
        return (f"Order {self.id} for {self.offer.name} by "
                f"{self.user_kyc.user.first_name} {self.user_kyc.user.last_name}")
