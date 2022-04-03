from django.urls import path

from task_manager.tasks.views import (
    TasksListPage,
    CreateTaskPage,
    ChangeTaskPage,
    DeleteTaskPage,
)
from task_manager.constants import (
    TASKS,
    CREATE_URL,
    UPDATE_URL,
    DELETE_URL,
    LIST,
    CREATE,
    CHANGE,
    DELETE,
)

app_name = TASKS
urlpatterns = [
    path("", TasksListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateTaskPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeTaskPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteTaskPage.as_view(), name=DELETE),
]
