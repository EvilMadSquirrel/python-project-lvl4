"""Tasks urls."""
from django.urls import path
from task_manager.constants import (
    CHANGE,
    CREATE,
    CREATE_URL,
    DELETE,
    DELETE_URL,
    DETAILS,
    DETAILS_URL,
    LIST,
    UPDATE_URL,
)
from task_manager.tasks.constants import TASKS
from task_manager.tasks.views import (
    ChangeTaskPage,
    CreateTaskPage,
    DeleteTaskPage,
    TaskDetailPage,
    TasksListPage,
)

app_name = TASKS
urlpatterns = [
    path("", TasksListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateTaskPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeTaskPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteTaskPage.as_view(), name=DELETE),
    path(DETAILS_URL, TaskDetailPage.as_view(), name=DETAILS),
]
