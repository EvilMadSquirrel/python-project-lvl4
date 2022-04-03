from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from task_manager.constants import (
    BUTTON_TEXT,
    INDEX,
    LOGGED_IN,
    LOGGED_OUT,
    LOGIN,
    LOGIN_BUTTON,
    LOGIN_TITLE,
    TITLE,
    VALUE_STRING,
)


class IndexPage(TemplateView):
    template_name = "index.html"


class LoginPage(SuccessMessageMixin, LoginView):
    template_name = "form.html"
    success_message = _(LOGGED_IN)
    next_page = reverse_lazy(INDEX)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(LOGIN_TITLE)
        context[BUTTON_TEXT] = _(LOGIN_BUTTON)
        context[VALUE_STRING] = LOGIN
        return context


class LogoutPage(LogoutView):
    next_page = reverse_lazy(INDEX)

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _(LOGGED_OUT))
        return super().dispatch(request, *args, **kwargs)
