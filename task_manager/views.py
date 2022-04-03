from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from task_manager.constants import (
    INDEX,
    LOGIN,
    TITLE,
    BUTTON_TEXT,
    LOGIN_BUTTON,
    LOGIN_TITLE,
    LOGGED_IN,
    LOGGED_OUT,
    VALUE,
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
        context[VALUE] = LOGIN
        return context


class LogoutPage(LogoutView):
    next_page = reverse_lazy(INDEX)

    def dispatch(self, request, *args, **kwargs):
        messages.add_message(request, messages.INFO, _(LOGGED_OUT))
        return super().dispatch(request, *args, **kwargs)
