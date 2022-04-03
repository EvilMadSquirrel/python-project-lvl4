from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

from task_manager.constants import (
    TASKS,
    TITLE,
    BUTTON_TEXT,
    DELETE_BUTTON,
    NOT_AUTHORIZED,
    TASK_CREATED_SUCCESSFULLY,
    TASK_CHANGED_SUCCESSFULLY,
    TASK_DELETED_SUCCESSFULLY,
    BY_ITS_AUTHOR,
    LOGIN,
    TASKS_LIST,
    CHANGE_TITLE,
    CREATE_TITLE,
    CREATE_TASK,
    CHANGE_TASK,
    DELETE_TASK,
    TASKS_TITLE, SHOW_TITLE,
)
from task_manager.tasks.models import Task
from task_manager.tasks.forms import TaskForm, TasksFilter


class TasksListPage(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks_list.html"
    context_object_name = TASKS
    filterset_class = TasksFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(TASKS_TITLE)
        context[BUTTON_TEXT] = _(SHOW_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class CreateTaskPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = _(TASK_CREATED_SUCCESSFULLY)

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CREATE_TASK)
        context[BUTTON_TEXT] = _(CREATE_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class ChangeTaskPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = _(TASK_CHANGED_SUCCESSFULLY)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CHANGE_TASK)
        context[BUTTON_TEXT] = _(CHANGE_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)


class DeleteTaskPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = _(TASK_DELETED_SUCCESSFULLY)

    def form_valid(self, form):
        if self.get_object().author != self.request.user:
            messages.error(self.request, _(BY_ITS_AUTHOR))
        else:
            super(DeleteTaskPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(DELETE_TASK)
        context[BUTTON_TEXT] = _(DELETE_BUTTON)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_AUTHORIZED))
        return redirect(LOGIN)
