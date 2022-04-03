from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.translations import (
    CHANGE_TITLE,
    CREATE_TITLE,
    DELETE_BUTTON,
    NOT_AUTHORIZED,
)
from task_manager.constants import BUTTON_TEXT, LOGIN, TITLE
from task_manager.statuses.translations import (
    CHANGE_STATUS,
    CREATE_STATUS,
    DELETE_STATUS,
    STATUS_CHANGED_SUCCESSFULLY,
    STATUS_CREATED_SUCCESSFULLY,
    STATUS_DELETED_SUCCESSFULLY,
    STATUS_IN_USE,
    STATUSES_TITLE,
)
from task_manager.statuses.constants import STATUSES, STATUSES_LIST
from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status


class StatusesListPage(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses_list.html"
    context_object_name = STATUSES

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = STATUSES_TITLE
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class CreateStatusPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_CREATED_SUCCESSFULLY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_STATUS
        context[BUTTON_TEXT] = CREATE_TITLE
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class ChangeStatusPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_CHANGED_SUCCESSFULLY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CHANGE_STATUS
        context[BUTTON_TEXT] = CHANGE_TITLE
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class DeleteStatusPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "delete.html"
    success_url = reverse_lazy(STATUSES_LIST)
    success_message = STATUS_DELETED_SUCCESSFULLY

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, STATUS_IN_USE)
        else:
            super(DeleteStatusPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_STATUS
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)
