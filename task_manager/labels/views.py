"""Views for labels with CRUD forms."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from ..mixins import HandleNoPermissionMixin
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


class LabelsListPage(
    LoginRequiredMixin,
    HandleNoPermissionMixin,
    ListView,
):
    """Labels list page."""

    model = Label
    template_name = "labels_list.html"
    context_object_name = LABELS
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

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


class CreateLabelPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    CreateView,
):
    """Create label page."""

    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_CREATED_SUCCESSFULLY
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

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


class ChangeLabelPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    UpdateView,
):
    """Change label page."""

    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_CHANGED_SUCCESSFULLY
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

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


class DeleteLabelPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    HandleNoPermissionMixin,
    DeleteView,
):
    """Delete label page."""

    model = Label
    template_name = "delete.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = LABEL_DELETED_SUCCESSFULLY
    no_permission_url = LOGIN
    error_message = NOT_AUTHORIZED

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
