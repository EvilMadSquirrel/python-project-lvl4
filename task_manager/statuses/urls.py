from django.urls import path
from task_manager.constants import (
    CHANGE,
    CREATE,
    DELETE,
    DELETE_URL,
    LIST,
    UPDATE_URL,
    CREATE_URL,
)
from task_manager.statuses.constants import STATUSES
from task_manager.statuses.views import (
    ChangeStatusPage,
    CreateStatusPage,
    DeleteStatusPage,
    StatusesListPage,
)

app_name = STATUSES
urlpatterns = [
    path("", StatusesListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateStatusPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeStatusPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteStatusPage.as_view(), name=DELETE),
]
