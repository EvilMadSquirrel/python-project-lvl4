"""Users urls."""
from django.urls import path
from task_manager.constants import (
    CHANGE,
    CREATE,
    CREATE_URL,
    DELETE,
    DELETE_URL,
    LIST,
    UPDATE_URL,
)
from task_manager.users.constants import USERS
from task_manager.users.views import (
    ChangeUserPage,
    CreateUserPage,
    DeleteUserPage,
    UsersListPage,
)

app_name = USERS
urlpatterns = [
    path("", UsersListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateUserPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeUserPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteUserPage.as_view(), name=DELETE),
]
