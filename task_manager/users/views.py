from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.users.forms import CreateUserForm
from task_manager.constants import (
    USERS,
    TITLE,
    LOGIN,
    USER_CREATED_SUCCESSFULLY,
    USER_CHANGED_SUCCESSFULLY,
    NOT_CHANGE_ANOTHER_USER,
    USER_IN_USE,
    USER_DELETED_SUCCESSFULLY,
    USERS_TITLE,
    CHANGE_TITLE,
    BUTTON_TEXT,
    DELETE_BUTTON,
    USERS_LIST,
    REGISTER,
    DELETE_USER,
    CHANGE_USER,
    CREATE_USER,
)


class UsersListPage(ListView):
    model = User
    template_name = "users_list.html"
    context_object_name = USERS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(USERS_TITLE)
        return context


class CreateUserPage(SuccessMessageMixin, CreateView):
    template_name = "form.html"
    form_class = CreateUserForm
    success_url = reverse_lazy(LOGIN)
    success_message = _(USER_CREATED_SUCCESSFULLY)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CREATE_USER)
        context[BUTTON_TEXT] = _(REGISTER)
        return context


class ChangeUserPage(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView
):
    model = User
    template_name = "form.html"
    form_class = CreateUserForm
    success_url = reverse_lazy(USERS_LIST)
    success_message = _(USER_CHANGED_SUCCESSFULLY)

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(CHANGE_USER)
        context[BUTTON_TEXT] = _(CHANGE_TITLE)
        return context

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_CHANGE_ANOTHER_USER))
        return redirect(USERS_LIST)


class DeleteUserPage(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, DeleteView
):
    model = User
    template_name = "delete.html"
    success_url = reverse_lazy(USERS_LIST)
    success_message = _(USER_DELETED_SUCCESSFULLY)

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[TITLE] = _(DELETE_USER)
        context[BUTTON_TEXT] = _(DELETE_BUTTON)
        return context

    def form_valid(self, form):
        if self.get_object().tasks.all() or self.get_object().tasks_in_work.all():
            messages.error(self.request, _(USER_IN_USE))
        else:
            super(DeleteUserPage, self).form_valid(form)
        return redirect(USERS_LIST)

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_CHANGE_ANOTHER_USER))
        return redirect(USERS_LIST)
