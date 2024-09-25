from django import forms
from django.forms import TextInput, ClearableFileInput, NumberInput, Select

from offers.models import Offer


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency name'}),
            "logo": ClearableFileInput(attrs={'class': 'form-control', "placeholder": "Insert cryptocurrency logo"}),
            "abbreviation": TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency abbreviation'}),
            "sell_price": NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency selling price'}),
            "buy_price": NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency buying price'}),
            "stock": NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency stock'}),
            "active": Select(attrs={'class': 'form-control', 'placeholder': 'Select cryptocurrency Online or Offline'}),

        }


class OfferUpdateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency name'}),
            "logo": ClearableFileInput(attrs={'class': 'form-control', "placeholder": "Insert cryptocurrency logo"}),
            "abbreviation": TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency abbreviation'}),
            "sell_price": NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency selling price'}),
            "buy_price": NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency buying price'}),
            "stock": NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter cryptocurrency stock'}),
            "active": Select(attrs={'class': 'form-control', 'placeholder': 'Select cryptocurrency Online or Offline'}),

        }
