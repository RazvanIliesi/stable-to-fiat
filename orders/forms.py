from django import forms

from orders.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']  # Include the fields you want to expose in the form
