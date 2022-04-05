"""Tests for users."""
from django.test import TestCase
from django.urls import reverse

from ..labels.models import Label
from ..statuses.models import Status
from ..tasks.models import Task
from .constants import (
    FIRST_NAME,
    LAST_NAME,
    LOGIN_TEST,
    PASSWORD1,
    PASSWORD2,
    USERNAME,
    USERS,
    USERS_CHANGE,
    USERS_CREATE,
    USERS_DELETE,
    USERS_LIST,
    USERS_TEST,
)
from .models import User
from .translations import (
    USER_CHANGED_SUCCESSFULLY,
    USER_CREATED_SUCCESSFULLY,
    USER_DELETED_SUCCESSFULLY,
)

STATUS_OK = 200


class TestUsers(TestCase):
    """Tests CRUD for users."""

    fixtures = ["users.json", "tasks.json", "statuses.json", "labels.json"]

    def setUp(self) -> None:
        """Get data from fixtures."""
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.label4 = Label.objects.get(pk=4)
        self.label5 = Label.objects.get(pk=5)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

    def test_users_list(self):
        """Check for all users in users page."""
        response = self.client.get(reverse(USERS_LIST))
        users_list = list(response.context[USERS])
        test_user1, test_user2 = users_list

        self.assertEqual(response.status_code, STATUS_OK)
        self.assertEqual(test_user1.username, "testuser1")
        self.assertEqual(test_user2.first_name, "First2")

    def test_user_create(self):
        """Check create new user."""
        url = reverse(USERS_CREATE)
        new_user = {
            USERNAME: "createdUser",
            FIRST_NAME: "createdFirst",
            LAST_NAME: "createdLast",
            PASSWORD1: "123",
            PASSWORD2: "123",
        }
        response = self.client.post(
            url,
            new_user,
            follow=True,
        )

        self.assertRedirects(response, LOGIN_TEST)

        self.assertContains(response, USER_CREATED_SUCCESSFULLY)
        created_user = User.objects.get(username=new_user[USERNAME])
        self.assertTrue(created_user.check_password("123"))

    def test_user_update(self):
        """Check change existing user."""
        user = self.user1
        self.client.force_login(user)
        url = reverse(USERS_CHANGE, args=(user.id,))
        new_data = {
            USERNAME: user.username,
            FIRST_NAME: user.first_name,
            LAST_NAME: user.last_name,
            PASSWORD1: "345",
            PASSWORD2: "345",
        }

        response = self.client.post(path=url, data=new_data, follow=True)
        self.assertRedirects(response, USERS_TEST)
        self.assertContains(response, USER_CHANGED_SUCCESSFULLY)
        changed_user = User.objects.get(username=user.username)
        self.assertTrue(changed_user.check_password("345"))

    def test_user_delete(self):
        """Test delete user."""
        Task.objects.all().delete()
        self.client.force_login(self.user1)
        url = reverse(USERS_DELETE, args=(self.user1.id,))
        response = self.client.post(url, follow=True)

        # noinspection PyTypeChecker
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user1.id)

        self.assertRedirects(response, USERS_TEST)
        self.assertContains(response, USER_DELETED_SUCCESSFULLY)
