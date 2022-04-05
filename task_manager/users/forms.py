"""Forms for users."""
from django.contrib.auth.forms import UserCreationForm
from task_manager.users.constants import (
    FIRST_NAME,
    LAST_NAME,
    PASSWORD1,
    PASSWORD2,
    USERNAME,
)
from task_manager.users.models import User


class CreateUserForm(UserCreationForm):
    """Form to create or update user."""

    class Meta:
        model = User
        fields = [
            FIRST_NAME,
            LAST_NAME,
            USERNAME,
            PASSWORD1,
            PASSWORD2,
        ]
