"""Views for users with CRUD forms."""
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.constants import BUTTON_TEXT, LOGIN, TITLE
from task_manager.translations import CHANGE_TITLE, DELETE_BUTTON
from task_manager.users.constants import USERS, USERS_LIST
from task_manager.users.forms import CreateUserForm
from task_manager.users.models import User
from task_manager.users.translations import (
    CHANGE_USER,
    CREATE_USER,
    DELETE_USER,
    NOT_CHANGE_ANOTHER_USER,
    REGISTER,
    USER_CHANGED_SUCCESSFULLY,
    USER_CREATED_SUCCESSFULLY,
    USER_DELETED_SUCCESSFULLY,
    USER_IN_USE,
    USERS_TITLE,
)


class UsersListPage(ListView):
    """Users list page."""

    model = User
    template_name = "users_list.html"
    context_object_name = USERS

    def get_context_data(self, **kwargs):
        """Add title text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = USERS_TITLE
        return context


class CreateUserPage(SuccessMessageMixin, CreateView):
    """Create user page."""

    template_name = "form.html"
    form_class = CreateUserForm
    success_url = reverse_lazy(LOGIN)
    success_message = USER_CREATED_SUCCESSFULLY

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = CREATE_USER
        context[BUTTON_TEXT] = REGISTER
        return context


class ChangeUserPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    UpdateView,
):
    """Change user page."""

    model = User
    template_name = "form.html"
    form_class = CreateUserForm
    success_url = reverse_lazy(USERS_LIST)
    success_message = USER_CHANGED_SUCCESSFULLY

    def test_func(self):
        """Checks user try to change yourself.

        Returns:
            (bool): Current user is user to change.
        """
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = CHANGE_USER
        context[BUTTON_TEXT] = CHANGE_TITLE
        return context

    def handle_no_permission(self):
        """Add error message and redirect to users page.

        Returns:
            Redirect to users page with message.
        """
        messages.error(self.request, NOT_CHANGE_ANOTHER_USER)
        return redirect(USERS_LIST)


class DeleteUserPage(
    LoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    DeleteView,
):
    """Delete user page."""

    model = User
    template_name = "delete.html"
    success_url = reverse_lazy(USERS_LIST)
    success_message = USER_DELETED_SUCCESSFULLY

    def test_func(self):
        """Checks user try to delete yourself.

        Returns:
            (bool): Current user is user to delete.
        """
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        """Add title and button text to context.

        Args:
            **kwargs: kwargs.

        Returns:
            Context.
        """
        context = super().get_context_data(**kwargs)
        context[TITLE] = DELETE_USER
        context[BUTTON_TEXT] = DELETE_BUTTON
        return context

    def form_valid(self, form):
        """Check if user is author or executor of any task.

        Args:
            form : User delete form.

        Returns:
            Redirect to users list with error message or HttpResponse.
        """
        if self.get_object().tasks.all() or self.get_object().works.all():
            messages.error(self.request, USER_IN_USE)
        else:
            super(DeleteUserPage, self).form_valid(form)
        return redirect(USERS_LIST)

    def handle_no_permission(self):
        """Add error message and redirect to users page.

        Returns:
            Redirect to users page with message.
        """
        messages.error(self.request, NOT_CHANGE_ANOTHER_USER)
        return redirect(USERS_LIST)
