from django.contrib import admin
from django.urls import include, path
from task_manager.constants import (
    ADMIN_URL,
    INDEX,
    LOGIN,
    LOGIN_URL,
    LOGOUT,
    LOGOUT_URL,
)
from task_manager.labels.constants import LABELS_URL
from task_manager.statuses.constants import STATUSES_URL
from task_manager.tasks.constants import TASKS_URL
from task_manager.users.constants import USERS_URL
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
