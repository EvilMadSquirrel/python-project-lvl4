from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.labels.forms import LabelForm
from task_manager.constants import (
    NOT_AUTHORIZED,
    LABEL_IN_USE,
    DELETE_BUTTON,
    LABEL_DELETED_SUCCESSFULLY,
    LABEL_CHANGED_SUCCESSFULLY,
    LABEL_CREATED_SUCCESSFULLY,
    CHANGE_TITLE,
    CREATE_TITLE,
    LOGIN,
    DELETE_LABEL,
    CHANGE_LABEL,
    CREATE_LABEL,
    LABELS_LIST,
    LABELS_TITLE,
    LABELS,
    BUTTON_TEXT,
    TITLE,
)


class LabelsListPage(LoginRequiredMixin, ListView):
    model = Label
    template_name = "labels_list.html"
    context_object_name = LABELS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(LABELS_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class CreateLabelPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = _(LABEL_CREATED_SUCCESSFULLY)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CREATE_LABEL)
        context[BUTTON_TEXT] = _(CREATE_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class ChangeLabelPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = _(LABEL_CHANGED_SUCCESSFULLY)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CHANGE_LABEL)
        context[BUTTON_TEXT] = _(CHANGE_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class DeleteLabelPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "delete.html"
    success_url = reverse_lazy(LABELS_LIST)
    success_message = _(LABEL_DELETED_SUCCESSFULLY)

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, _(LABEL_IN_USE))
        else:
            super(DeleteLabelPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(DELETE_LABEL)
        context[BUTTON_TEXT] = _(DELETE_BUTTON)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)
