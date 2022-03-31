from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Label
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class TestLabels(TestCase):
    fixtures = ["labels.json", "tasks.json", "users.json", "statuses.json"]

    def setUp(self) -> None:
        self.user = User.objects.get(pk=1)

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.label4 = Label.objects.get(pk=4)
        self.label5 = Label.objects.get(pk=5)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

    def test_labels_list(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("labels:list"))
        self.assertEqual(response.status_code, 200)
        labels_list = list(response.context["labels"])
        self.assertQuerysetEqual(
            labels_list,
            [
                self.label1,
                self.label2,
                self.label3,
                self.label4,
                self.label5,
            ],
        )

    def test_labels_list_no_login(self):
        response = self.client.get(reverse("labels:list"))
        self.assertRedirects(response, "/login/")

    def test_create_label(self):
        self.client.force_login(self.user)
        label = {"name": "label6"}
        response = self.client.post(reverse("labels:create"), label, follow=True)
        self.assertRedirects(response, "/labels/")
        self.assertContains(response, _("Label created successfully"))
        created_label = Label.objects.get(name=label["name"])
        self.assertEquals(created_label.name, "label6")

    def test_change_label(self):
        self.client.force_login(self.user)
        url = reverse("labels:change", args=(self.label1.pk,))
        new_label = {"name": "changed"}
        response = self.client.post(url, new_label, follow=True)
        self.assertRedirects(response, "/labels/")
        self.assertContains(response, _("Label changed successfully"))
        self.assertEqual(Label.objects.get(pk=self.label1.id), self.label1)

    def test_label_with_tasks_delete(self):
        self.client.force_login(self.user)
        url = reverse("labels:delete", args=(self.label1.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Label.objects.filter(pk=self.label1.id).exists())
        self.assertRedirects(response, "/labels/")
        self.assertContains(response, _("Cannot delete label because it is in use"))

    def test_delete_status(self):
        self.client.force_login(self.user)
        Task.objects.all().delete()
        url = reverse("labels:delete", args=(self.label1.pk,))
        response = self.client.post(url, follow=True)
        # noinspection PyTypeChecker
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=self.label1.pk)
        self.assertRedirects(response, "/labels/")
        self.assertContains(response, _("Label deleted successfully"))
