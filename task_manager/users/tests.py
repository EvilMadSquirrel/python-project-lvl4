from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User


class TestUsers(TestCase):
    fixtures = ["users.json"]

    def setUp(self) -> None:
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

    def test_users_list(self):
        response = self.client.get(reverse("users:list"))
        users_list = list(response.context["users"])
        test_user1, test_user2 = users_list

        self.assertEqual(response.status_code, 200)
        self.assertEqual(test_user1.username, "testuser1")
        self.assertEqual(test_user2.first_name, "Test2")

    def test_user_create(self):
        url = reverse("users:create")
        new_user = {
            "username": "createdUser",
            "first_name": "createdFirst",
            "last_name": "createdLast",
            "password1": "123",
            "password2": "123",
        }
        response = self.client.post(
            url,
            new_user,
            follow=True,
        )

        self.assertRedirects(response, "/login/")

        self.assertContains(response, _("User created successfully"))
        created_user = User.objects.get(username=new_user["username"])
        self.assertTrue(created_user.check_password("123"))

    def test_user_update(self):
        user = self.user1
        self.client.force_login(user)
        url = reverse("users:change", args=(user.id,))
        new_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "password1": "345",
            "password2": "345",
        }

        response = self.client.post(path=url, data=new_data, follow=True)
        self.assertRedirects(response, "/users/")
        self.assertContains(response, _("User changed successfully"))
        changed_user = User.objects.get(username=user.username)
        self.assertTrue(changed_user.check_password("345"))

    def test_user_delete(self):
        self.client.force_login(self.user1)
        url = reverse("users:delete", args=(self.user1.id,))
        response = self.client.post(url, follow=True)

        # noinspection PyTypeChecker
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user1.id)

        self.assertRedirects(response, "/users/")
        self.assertContains(response, _("User deleted successfully"))
