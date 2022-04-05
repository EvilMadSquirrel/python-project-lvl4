"""Statuses urls."""
from django.urls import path

from .constants import (
    CHANGE,
    CREATE,
    CREATE_URL,
    DELETE,
    DELETE_URL,
    LIST,
    STATUSES,
    UPDATE_URL,
)
from .views import (
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
