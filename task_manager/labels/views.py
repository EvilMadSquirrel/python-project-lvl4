from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.constants import (
    BUTTON_TEXT,
    CHANGE_TITLE,
    CREATE_TITLE,
    DELETE_BUTTON,
    LOGIN,
    NOT_AUTHORIZED,
    TITLE,
)
from task_manager.labels.constants import (
    CHANGE_LABEL,
    CREATE_LABEL,
    DELETE_LABEL,
    LABEL_CHANGED_SUCCESSFULLY,
    LABEL_CREATED_SUCCESSFULLY,
    LABEL_DELETED_SUCCESSFULLY,
    LABEL_IN_USE,
    LABELS,
    LABELS_LIST,
    LABELS_TITLE,
)
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label


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
