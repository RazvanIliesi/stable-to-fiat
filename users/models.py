from django.contrib.auth.models import User
from django.db import models


class UserKYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    personal_id = models.ImageField(upload_to='users_ids/')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.username})"






