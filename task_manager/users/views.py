from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .forms import CreateUserForm


class UsersListPage(ListView):
    model = User
    template_name = "users_list.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Users")
        return context


class CreateUserPage(SuccessMessageMixin, CreateView):
    template_name = "form.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("login")
    success_message = _("User created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create user")
        context["button_text"] = _("Register")
        return context


class ChangeUserPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    template_name = "form.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("users:list")
    success_message = _("User changed successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Change user")
        context["button_text"] = _("Change")
        return context


class DeleteUserPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "delete.html"
    success_url = reverse_lazy("users:list")
    success_message = _("User deleted successfully")

    def form_valid(self, form):
        if self.get_object().tasks.all() or self.get_object().tasks_in_work.all():
            messages.error(self.request, _("Cannot delete user because it is in use"))
        elif self.get_object() != self.request.user:
            messages.error(self.request, _("You do not have permission to change another user"))
        else:
            super(DeleteUserPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete user")
        context["button_text"] = _("Yes, delete")
        return context
