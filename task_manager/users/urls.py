from django.urls import path

from task_manager.constants import (
    USERS,
    LIST,
    CREATE_URL,
    UPDATE_URL,
    DELETE_URL,
    CREATE,
    CHANGE,
    DELETE,
)
from task_manager.users.views import (
    UsersListPage,
    CreateUserPage,
    ChangeUserPage,
    DeleteUserPage,
)

app_name = USERS
urlpatterns = [
    path("", UsersListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateUserPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeUserPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteUserPage.as_view(), name=DELETE),
]
