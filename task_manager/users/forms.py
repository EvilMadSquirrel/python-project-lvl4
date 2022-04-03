from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from task_manager.constants import (
    PASSWORD_2,
    PASSWORD_1,
    USERNAME,
    LAST_NAME,
    FIRST_NAME,
)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            FIRST_NAME,
            LAST_NAME,
            USERNAME,
            PASSWORD_1,
            PASSWORD_2,
        ]
