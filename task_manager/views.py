from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy


class IndexPage(TemplateView):
    template_name = "index.html"


class LoginPage(SuccessMessageMixin, LoginView):
    template_name = "form.html"
    success_message = _("Successfully logged in")
    next_page = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Log in")
        context["button_text"] = _("Login")
        context["value"] = "login"
        return context


class LogoutPage(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)
