from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import get_template

from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView

from StableToFiat.settings import DEFAULT_FROM_EMAIL
from users.forms import UserForm, UserVerificationForm, UserProfileForm
from users.models import UserKYC


class UserCreateView(CreateView):
    template_name = 'users/create_user.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.first_name = new_user.first_name.title()
            new_user.last_name = new_user.last_name.title()
            new_user.is_active = False
            new_user.save()

            subject = 'Create a new user'
            message = f'Hello, {new_user.first_name} {new_user.last_name}\n Your username: {new_user.username}.'

            token = default_token_generator.make_token(new_user)  # generare token pentru utilizator
            uid = urlsafe_base64_encode(force_bytes(new_user.id))  #
            activation_url = self.request.build_absolute_uri(
                reverse_lazy('activate', kwargs={'uid64': uid, 'token': token})
            )
            subject = 'Activate your account!'

            details_user = {
                'fullname': f'{new_user.first_name} {new_user.last_name}',
                'user_name': new_user.username,
                'activation_url': activation_url
            }

            message = get_template('email.html').render(details_user)
            mail = EmailMessage(subject, message, DEFAULT_FROM_EMAIL, [new_user.email])
            mail.content_subtype = 'html'
            mail.send()

        return redirect('login')


def activate_user(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = get_object_or_404(User,
                                 pk=uid)

    except User.DoesNotExist:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return HttpResponse('Nu exista')


class UserProfile(DetailView):
    template_name = "users/user_profile.html"

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        user_kyc = get_object_or_404(UserKYC, user=user)

        context['user'] = user
        context['user_kyc'] = user_kyc
        return context


class UserVerificationCreateView(CreateView):
    template_name = 'users/user_verification.html'
    model = UserKYC
    form_class = UserVerificationForm
    success_url = reverse_lazy('user-verification-done')
    login_url = reverse_lazy('login')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)


class UserVerificationDoneView(TemplateView):
    template_name = "users/user_verification_done.html"


class EditProfileView(UpdateView):
    template_name = 'users/edit_profile.html'
    form_class = UserProfileForm

    def get_object(self):
        user_id = self.kwargs.get('pk')
        return get_object_or_404(User, pk=user_id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        user_id = self.object.id
        return reverse_lazy('user-profile', args=[user_id])

