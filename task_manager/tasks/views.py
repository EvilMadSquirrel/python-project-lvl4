from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView
from task_manager.constants import BUTTON_TEXT, LOGIN, TITLE
from task_manager.tasks.constants import TASKS, TASKS_LIST
from task_manager.tasks.forms import TaskForm, TasksFilter
from task_manager.tasks.models import Task
from task_manager.tasks.translations import (
    BY_ITS_AUTHOR,
    CHANGE_TASK,
    CREATE_TASK,
    DELETE_TASK,
    SHOW_TITLE,
    TASK_CHANGED_SUCCESSFULLY,
    TASK_CREATED_SUCCESSFULLY,
    TASK_DELETED_SUCCESSFULLY,
    TASKS_TITLE,
)
from task_manager.translations import (
    CHANGE_TITLE,
    CREATE_TITLE,
    DELETE_BUTTON,
    NOT_AUTHORIZED,
)


class TasksListPage(LoginRequiredMixin, FilterView):
    model = Task
    template_name = "tasks_list.html"
    context_object_name = TASKS
    filterset_class = TasksFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = TASKS_TITLE
        context[BUTTON_TEXT] = SHOW_TITLE
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class CreateTaskPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_CREATED_SUCCESSFULLY

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_TASK
        context[BUTTON_TEXT] = CREATE_TITLE
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class ChangeTaskPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_CHANGED_SUCCESSFULLY

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = CHANGE_TASK
        context[BUTTON_TEXT] = CHANGE_TITLE
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)


class DeleteTaskPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy(TASKS_LIST)
    success_message = TASK_DELETED_SUCCESSFULLY

    def form_valid(self, form):
        if self.request.user == self.get_object().author:
            super(DeleteTaskPage, self).form_valid(form)
        else:
            messages.error(self.request, BY_ITS_AUTHOR)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_TASK
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context

    def handle_no_permission(self):
        messages.error(self.request, NOT_AUTHORIZED)
        return redirect(LOGIN)
