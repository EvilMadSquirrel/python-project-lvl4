from django.urls import path

from task_manager.constants import (
    DELETE_URL,
    UPDATE_URL,
    CREATE_URL,
    STATUSES,
    LIST,
    CREATE,
    CHANGE,
    DELETE,
)
from task_manager.statuses.views import (
    StatusesListPage,
    ChangeStatusPage,
    CreateStatusPage,
    DeleteStatusPage,
)

app_name = STATUSES
urlpatterns = [
    path("", StatusesListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateStatusPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeStatusPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteStatusPage.as_view(), name=DELETE),
]
