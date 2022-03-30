from django.urls import path

from .views import TasksListPage, CreateTaskPage, ChangeTaskPage, DeleteTaskPage

app_name = "tasks"
urlpatterns = [
    path("", TasksListPage.as_view(), name="list"),
    path("create/", CreateTaskPage.as_view(), name="create"),
    path("<int:pk>/update/", ChangeTaskPage.as_view(), name="change"),
    path("<int:pk>/delete/", DeleteTaskPage.as_view(), name="delete"),
]
