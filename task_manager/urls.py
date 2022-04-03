from django.contrib import admin
from django.urls import include, path

from task_manager.constants import (
    ADMIN_URL,
    LABELS_URL,
    TASKS_URL,
    STATUSES_URL,
    USERS_URL,
    LOGOUT_URL,
    LOGIN_URL,
    LOGIN,
    LOGOUT,
    INDEX,
)
from task_manager.views import IndexPage, LoginPage, LogoutPage

urlpatterns = [
    path("", IndexPage.as_view(), name=INDEX),
    path(LOGIN_URL, LoginPage.as_view(), name=LOGIN),
    path(LOGOUT_URL, LogoutPage.as_view(), name=LOGOUT),
    path(USERS_URL, include("task_manager.users.urls")),
    path(STATUSES_URL, include("task_manager.statuses.urls")),
    path(TASKS_URL, include("task_manager.tasks.urls")),
    path(LABELS_URL, include("task_manager.labels.urls")),
    path(ADMIN_URL, admin.site.urls),
]
