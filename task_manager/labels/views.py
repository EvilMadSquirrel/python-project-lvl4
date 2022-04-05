"""Views for labels with CRUD forms."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .constants import BUTTON_TEXT, LABELS, LABELS_LIST, LOGIN, TITLE
from .forms import LabelForm
from .models import Label
from .translations import (
    CHANGE_LABEL,
    CHANGE_TITLE,
    CREATE_LABEL,
    CREATE_TITLE,
    DELETE_BUTTON,
    DELETE_LABEL,
    LABEL_CHANGED_SUCCESSFULLY,
    LABEL_CREATED_SUCCESSFULLY,
    LABEL_DELETED_SUCCESSFULLY,
    LABEL_IN_USE,
    LABELS_TITLE,
    NOT_AUTHORIZED,
)


class LabelsListPage(LoginRequiredMixin, ListView):
    """Labels list page."""

    model = Label
    template_name = "labels_list.html"
    context_object_name = LABELS

    def get_context_data(self, **kwargs):
        """Add title text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = LABELS_TITLE
        return context

    def handle_no_permission(self):
        """Add error message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class CreateLabelPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """Create label page."""

    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_CREATED_SUCCESSFULLY

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_LABEL
        context[BUTTON_TEXT] = CREATE_TITLE
        return context

    def handle_no_permission(self):
        """Add error message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class ChangeLabelPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Change label page."""

    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_CHANGED_SUCCESSFULLY

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = CHANGE_LABEL
        context[BUTTON_TEXT] = CHANGE_TITLE
        return context

    def handle_no_permission(self):
        """Add ERROR message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class DeleteLabelPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """Delete label page."""

    model = Label
    template_name = "delete.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_DELETED_SUCCESSFULLY

    def form_valid(self, form):
        """Check if label has tasks.

        Args:
            form: Label delete form.

        Returns:
            Redirect to labels with error message or HttpResponse.
        """
        if self.get_object().tasks.all():
            messages.error(self.request, LABEL_IN_USE)
        else:
            super(DeleteLabelPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_LABEL
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context

    def handle_no_permission(self):
        """Add error message and redirect to login page.

        Returns:
            Redirect to login page with message.
        """
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)
