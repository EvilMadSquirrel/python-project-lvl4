"""Mixins module."""
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class HandleNoPermissionMixin(AccessMixin):
    """Redirect to login page mixin."""

    no_permission_url = ""
    error_message = ""

    def handle_no_permission(self):
        """Add error message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, self.error_message)
        return redirect(self.no_permission_url)
