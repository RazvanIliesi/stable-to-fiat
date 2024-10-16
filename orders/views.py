from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView

from offers.models import Offer
from orders.forms import OrderForm
from orders.models import Order
from users.models import UserKYC


class BaseOrderView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/create_order.html'  # Your template for order creation
    success_url = reverse_lazy('order-success')  # Redirect after successful order creation

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

        # Set the order instance
        order = form.save(commit=False)
        order.user_kyc = user_kyc
        order.offer = offer

        # Set the price from the offer based on the order type
        if order.order_type == "sell":
            order.price = offer.sell_price
        elif order.order_type == "buy":
            order.price = offer.buy_price
        else:
            return HttpResponseForbidden("Invalid order type.")

        # Save the order instance
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

        # Save the order instance to the database
        return super().form_valid(form)  # Calls the base form_valid which handles saving and redirecting

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_type'] = 'buy'
        return context


class OrderSuccessView(TemplateView):
    template_name = 'orders/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add a success message to the context
        context['success_message'] = "Your order has been placed successfully! Thank you for your purchase."
        return context


class OrderListView(ListView):
    template_name = "orders/orders_list.html"
    model = Order
    context_object_name = "all_orders"


class ChangeOrderStatusView(View):
    def post(self, request, order_id):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You must be logged in to update the order status.")

        # Get the order by its ID (this ID is coming from the URL)
        order = get_object_or_404(Order, id=order_id)

        # Get the new status from the POST request data
        new_status = request.POST.get("status")

        # Update the order's status if it's a valid option
        if new_status in ["complete", "canceled"]:  # Only allow valid statuses
            order.status = new_status
            order.save()

        # Redirect to the order list or any desired view
        return redirect('order-list')  # Replace with the appropriate view name