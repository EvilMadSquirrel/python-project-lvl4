from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from .models import Status


class TestStatuses(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)

    def test_statuses_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("statuses:list"))
        self.assertEqual(response.status_code, 200)
        statuses_list = list(response.context["statuses"])
        self.assertQuerysetEqual(statuses_list, [self.status1, self.status2])

    def test_statuses_list_no_login(self):
        response = self.client.get(reverse("statuses:list"))
        self.assertRedirects(
            response,
            "/login/",
        )

    def test_create_status(self):
        self.client.force_login(self.user)
        status = {"name": "status3"}
        response = self.client.post(reverse("statuses:create"), status, follow=True)
        self.assertRedirects(
            response,
            "/statuses/",
        )
        self.assertContains(response, _("Status created successfully"))
        created_status = Status.objects.get(name=status["name"])
        self.assertEquals(created_status.name, "status3")

    def test_change_status(self):
        self.client.force_login(self.user)
        url = reverse("statuses:change", args=(self.status1.id,))
        new_status = {"name": "status4"}
        response = self.client.post(url, new_status, follow=True)
        self.assertRedirects(
            response,
            "/statuses/",
        )
        self.assertContains(response, _("Status changed successfully"))
        self.assertEqual(Status.objects.get(pk=self.status1.id), self.status1)

    def test_delete_status(self):
        self.client.force_login(self.user)
        url = reverse("statuses:delete", args=(self.status1.id,))
        response = self.client.post(url, follow=True)
        # noinspection PyTypeChecker
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(pk=self.status1.id)
        self.assertRedirects(
            response,
            "/statuses/",
        )
        self.assertContains(response, _("Status deleted successfully"))
