from django.urls import path

from .views import UsersListPage, CreateUserPage, ChangeUserPage, DeleteUserPage
app_name = "users"
urlpatterns = [
    path("", UsersListPage.as_view(), name="list"),
    path("create/", CreateUserPage.as_view(), name="create"),
    path("<int:pk>/update/", ChangeUserPage.as_view(), name="change"),
    path("<int:pk>/delete/", DeleteUserPage.as_view(), name="delete"),
]
