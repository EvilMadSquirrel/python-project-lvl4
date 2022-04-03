from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.statuses.models import Status
from task_manager.statuses.forms import StatusForm
from task_manager.constants import (
    NOT_AUTHORIZED,
    STATUSES_TITLE,
    LOGIN,
    STATUS_CREATED_SUCCESSFULLY,
    STATUSES_LIST,
    STATUS_IN_USE,
    STATUS_DELETED_SUCCESSFULLY,
    STATUS_CHANGED_SUCCESSFULLY,
    CHANGE_TITLE,
    CREATE_TITLE,
    DELETE_BUTTON,
    DELETE_STATUS,
    CHANGE_STATUS,
    CREATE_STATUS,
    STATUSES,
    TITLE,
    BUTTON_TEXT,
)


class StatusesListPage(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses_list.html"
    context_object_name = STATUSES

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(STATUSES_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class CreateStatusPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = _(STATUS_CREATED_SUCCESSFULLY)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CREATE_STATUS)
        context[BUTTON_TEXT] = _(CREATE_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class ChangeStatusPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = _(STATUS_CHANGED_SUCCESSFULLY)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CHANGE_STATUS)
        context[BUTTON_TEXT] = _(CHANGE_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class DeleteStatusPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "delete.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = _(STATUS_DELETED_SUCCESSFULLY)

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, _(STATUS_IN_USE))
        else:
            super(DeleteStatusPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(DELETE_STATUS)
        context[BUTTON_TEXT] = _(DELETE_BUTTON)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)
