"""Labels urls."""
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
from task_manager.labels.constants import LABELS
from task_manager.labels.views import (
    ChangeLabelPage,
    CreateLabelPage,
    DeleteLabelPage,
    LabelsListPage,
)

app_name = LABELS
urlpatterns = [
    path("", LabelsListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateLabelPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeLabelPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteLabelPage.as_view(), name=DELETE),
]
