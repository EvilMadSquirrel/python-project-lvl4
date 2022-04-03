from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from task_manager.users.constants import (
    FIRST_NAME,
    LAST_NAME,
    PASSWORD1,
    PASSWORD2,
    USERNAME,
)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            FIRST_NAME,
            LAST_NAME,
            USERNAME,
            PASSWORD1,
            PASSWORD2,
        ]
