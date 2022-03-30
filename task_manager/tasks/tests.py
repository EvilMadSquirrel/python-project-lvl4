from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Task
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class TestTasks(TestCase):
    fixtures = ["tasks.json", "statuses.json", "users.json"]

    def setUp(self) -> None:
        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)

    def test_tasks_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse("tasks:list"))
        self.assertEqual(response.status_code, 200)
        tasks_list = list(response.context["tasks"])
        self.assertQuerysetEqual(tasks_list, [self.task1, self.task2])

    def test_tasks_list_no_login(self):
        response = self.client.get(reverse("tasks:list"))
        self.assertRedirects(response, "/login/")

    def test_create_task(self):
        self.client.force_login(self.user1)
        task = {
            "name": "task3",
            "description": "description3",
            "status": self.status1,
            "author": self.user1,
            "executor": self.user2,
        }
        response = self.client.post(reverse("tasks:create"), task, follow=True)
        self.assertRedirects(response, "/tasks/")
        self.assertContains(response, _("Task created successfully"))
        created_task = Status.objects.get(name=task["name"])
        self.assertEquals(created_task.name, "task3")

    def test_change_task(self):
        self.client.force_login(self.user1)
        url = reverse("tasks:change", args=(self.task1.pk,))
        changed_task = {
            "name": self.task1.name,
            "description": "changed description",
            "status": self.task1.status,
            "author": self.user1,
            "executor": self.task1.executor,
        }
        response = self.client.post(url, changed_task, follow=True)
        self.assertRedirects(response, "/tasks/")
        self.assertContains(response, _("Task changed successfully"))
        self.assertEqual(Task.objects.get(pk=self.task1.pk), self.task1)

    def test_delete_task(self):
        self.client.force_login(self.user1)
        url = reverse("tasks:delete", args=(self.task1.pk,))
        response = self.client.post(url, follow=True)
        # noinspection PyTypeChecker
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.pk)
        self.assertRedirects(response, "/tasks/")
        self.assertContains(response, _("Task deleted successfully"))

    def test_delete_task_not_author(self):
        self.client.force_login(self.user1)
        url = reverse("tasks:delete", args=(self.task2.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())
        self.assertRedirects(response, "/tasks/")
        self.assertContains(response, _("A task can only be deleted by its author."))
