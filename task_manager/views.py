"""Views for index, login and logout pages."""
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from .constants import BUTTON_TEXT, INDEX, TITLE
from .translations import LOGGED_IN, LOGGED_OUT, LOGIN_BUTTON, LOGIN_TITLE


class IndexPage(TemplateView):
    """Index page view."""

    template_name = "index.html"


class LoginPage(SuccessMessageMixin, LoginView):
    """Login page view."""

    template_name = "form.html"
    success_message = LOGGED_IN
    next_page = reverse_lazy(INDEX)

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = LOGIN_TITLE
        context[BUTTON_TEXT] = LOGIN_BUTTON
        return context


class LogoutPage(LogoutView):
    """Logout page view."""

    next_page = reverse_lazy(INDEX)

    def dispatch(self, request, *args, **kwargs):
        """Add logout message.

        Args:
            request: HTTP request.
            *args: args.
            **kwargs: kwargs.

        Returns:
            Inherited method with message.
        """
        messages.add_message(request, messages.INFO, LOGGED_OUT)
        return super().dispatch(request, *args, **kwargs)
