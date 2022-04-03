from django.urls import path
from task_manager.constants import (
    DELETE_URL,
    UPDATE_URL,
    CREATE_URL,
    LABELS,
    LIST,
    CREATE,
    CHANGE,
    DELETE,
)
from task_manager.labels.views import (
    LabelsListPage,
    ChangeLabelPage,
    CreateLabelPage,
    DeleteLabelPage,
)

app_name = LABELS
urlpatterns = [
    path("", LabelsListPage.as_view(), name=LIST),
    path(CREATE_URL, CreateLabelPage.as_view(), name=CREATE),
    path(UPDATE_URL, ChangeLabelPage.as_view(), name=CHANGE),
    path(DELETE_URL, DeleteLabelPage.as_view(), name=DELETE),
]
