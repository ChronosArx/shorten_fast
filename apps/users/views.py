from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import CustomAuthenticationForm, UserRegisterForm


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("users:login")


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"
    redirect_authenticated_user = True


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "profile.html"
