from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.constants import (
    BUTTON_TEXT,
    CHANGE_TITLE,
    DELETE_BUTTON,
    LOGIN,
    TITLE,
)
from task_manager.users.constants import (
    CHANGE_USER,
    CREATE_USER,
    DELETE_USER,
    NOT_CHANGE_ANOTHER_USER,
    REGISTER,
    USER_CHANGED_SUCCESSFULLY,
    USER_CREATED_SUCCESSFULLY,
    USER_DELETED_SUCCESSFULLY,
    USER_IN_USE,
    USERS,
    USERS_LIST,
    USERS_TITLE,
)
from task_manager.users.forms import CreateUserForm


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
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    UpdateView,
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
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    DeleteView,
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
        if self.get_object().tasks.all() or self.get_object().works.all():
            messages.error(self.request, _(USER_IN_USE))
        else:
            super(DeleteUserPage, self).form_valid(form)
        return redirect(USERS_LIST)

    def handle_no_permission(self):
        messages.error(self.request, _(NOT_CHANGE_ANOTHER_USER))
        return redirect(USERS_LIST)
