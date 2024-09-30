from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from offers.models import Offer
from orders.forms import OrderForm
from orders.models import Order
from users.models import UserKYC


class BaseOrderView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'  # Your template for order creation
    success_url = reverse_lazy('order_success')  # Redirect after successful order creation

    def form_valid(self, form):
        # Ensure the user is authenticated
        if not self.request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to create an order.")

        # Get user KYC information
        user_kyc = get_object_or_404(UserKYC, user=self.request.user)

        # Check if the user is verified
        if not user_kyc.is_verified:
            return HttpResponseForbidden("User not verified. Cannot create order.")

        # Get the offer from the URL parameters
        offer_id = self.kwargs['offer_id']  # Assume the offer ID is passed as part of the URL
        offer = get_object_or_404(Offer, id=offer_id)

        # Set the user_kyc and offer in the form's cleaned data
        order = form.save(commit=False)
        order.user_kyc = user_kyc
        order.offer = offer

        # Set the price from the offer
        order.price = offer.sell_price if order.order_type == "sell" else offer.buy_price

        order.save()

        return super().form_valid(form)


class SellOrderView(BaseOrderView):
    def form_valid(self, form):
        # Set the order type to "sell"
        order = form.save(commit=False)
        order.order_type = "sell"  # Set the order type to sell
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_type'] = 'sell'
        return context


class BuyOrderView(BaseOrderView):
    def form_valid(self, form):
        # Set the order type to "buy"
        order = form.save(commit=False)
        order.order_type = "buy"  # Set the order type to buy
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_type'] = 'buy'
        return context
