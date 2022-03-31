from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm


class TasksListPage(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Tasks")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class CreateTaskPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy("tasks:list")
    success_message = _("Task created successfully")

    def form_valid(self, form):
        form.instance.author = User.objects.get(pk=self.request.user.pk)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create task")
        context["button_text"] = _("Create")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class ChangeTaskPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "form.html"
    success_url = reverse_lazy("tasks:list")
    success_message = _("Task changed successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Change task")
        context["button_text"] = _("Change")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class DeleteTaskPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = "delete.html"
    success_url = reverse_lazy("tasks:list")
    success_message = _("Task deleted successfully")

    def form_valid(self, form):
        if self.get_object().author != self.request.user:
            messages.error(self.request, _("A task can only be deleted by its author"))
        else:
            super(DeleteTaskPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete task")
        context["button_text"] = _("Delete")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")
