from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User

from django import forms

from users.models import UserKYC


class AuthenticationNewForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter an Username'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter an Password'})


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your username'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your first name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your last name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Please enter your email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter a password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter a password confirmation'})


class PasswordResetNewForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your email'})


class SetPasswordNewForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your new password'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please confirm your new password'})


class UserVerificationForm(forms.ModelForm):
    class Meta:
        model = UserKYC
        fields = ["address", "city", "state", "country", "phone_number", "personal_id"]

        widgets = {
            "address": forms.TextInput(
                attrs={'class': 'form-control', "placeholder": "Please enter your full address"}),
            "city": forms.TextInput(attrs={'class': 'form-control', "placeholder": "Please enter your city"}),
            "state": forms.TextInput(attrs={'class': 'form-control', "placeholder": "Please enter your state"}),
            "country": forms.TextInput(attrs={'class': 'form-control', "placeholder": "Please enter your country"}),
            "phone_number": forms.TextInput(
                attrs={'class': 'form-control', "placeholder": "Please enter your phone number"}),
            "personal_id": forms.ClearableFileInput(
                attrs={'class': 'form-control', "placeholder": "Please enter your personal id"}),
        }


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your first name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your last name'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    class Meta:
        model = UserKYC
        fields = ['address', 'city', 'state', 'country', 'phone_number', 'personal_id']
        widgets = {
            "address": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your full address'
            }),
            "city": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your city'
            }),
            "state": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your state'
            }),
            "country": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your country'
            }),
            "phone_number": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your phone number'
            }),
            "personal_id": forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please upload your personal ID'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        self.fields = {
            'first_name': self.fields['first_name'],
            'last_name': self.fields['last_name'],
            'email': self.fields['email'],
            **self.fields,
        }
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        user = self.get_user()
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            user_kyc = UserKYC.objects.get(user=user)
            user_kyc.address = self.cleaned_data['address']
            user_kyc.city = self.cleaned_data['city']
            user_kyc.state = self.cleaned_data['state']
            user_kyc.country = self.cleaned_data['country']
            user_kyc.phone_number = self.cleaned_data['phone_number']
            user_kyc.personal_id = self.cleaned_data['personal_id']
            user_kyc.save()
        return user

    def get_user(self):
        return User.objects.get(pk=self.instance.user.id)