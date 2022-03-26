from django.urls import path

from .views import (
    StatusesListPage,
    ChangeStatusPage,
    CreateStatusPage,
    DeleteStatusPage,
)

app_name = "statuses"
urlpatterns = [
    path("", StatusesListPage.as_view(), name="list"),
    path("create/", CreateStatusPage.as_view(), name="create"),
    path("<int:pk>/update/", ChangeStatusPage.as_view(), name="change"),
    path("<int:pk>/delete/", DeleteStatusPage.as_view(), name="delete"),
]
