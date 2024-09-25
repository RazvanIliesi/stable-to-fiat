from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from offers.forms import OfferForm, OfferUpdateForm
from offers.models import Offer


class OffersCreateView(CreateView):
    template_name = "offers/create_offer.html"
    model = Offer
    form_class = OfferForm
    success_url = reverse_lazy("offers-list")


class OffersListView(ListView):
    template_name = "offers/offers_list.html"
    model = Offer
    context_object_name = "all_offers"


class OfferUpdateView(UpdateView):
    template_name = "offers/update_offers.html"
    model = Offer
    form_class = OfferUpdateForm
    success_url = reverse_lazy("offers-list")


class OfferDeleteView(DeleteView):
    template_name = "offers/delete_offers.html"
    model = Offer
    success_url = reverse_lazy("offers-list")

