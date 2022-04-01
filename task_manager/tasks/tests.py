from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .models import Task
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class TestTasks(TestCase):
    fixtures = ["tasks.json", "statuses.json", "users.json", "labels.json"]

    def setUp(self) -> None:
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.label4 = Label.objects.get(pk=4)
        self.label5 = Label.objects.get(pk=5)

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.task = {
            "name": "task3",
            "description": "description3",
            "status": 1,
            "author": 1,
            "executor": 2,
            "labels": [1, 2],
        }

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
        response = self.client.post(reverse("tasks:create"), self.task, follow=True)
        self.assertRedirects(response, "/tasks/")
        self.assertContains(response, _("Task created successfully"))
        created_task = Task.objects.get(name=self.task["name"])
        self.assertEquals(created_task.name, "task3")

    def test_change_task(self):
        self.client.force_login(self.user1)
        url = reverse("tasks:change", args=(self.task1.pk,))
        changed_task = {
            "name": "changed name",
            "description": "changed description",
            "status": 1,
            "author": 1,
            "executor": 2,
            "labels": [3, 4, 5],
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
        self.assertContains(response, _("A task can only be deleted by its author"))

    def test_filter_self_tasks(self):
        self.client.force_login(self.user1)
        filtered_list = '{0}?self_task=on'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.task1])

    def test_filter_by_status(self):
        self.client.force_login(self.user1)
        filtered_list = '{0}?status=2'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.task2])

    def test_filter_by_executor(self):
        self.client.force_login(self.user1)
        filtered_list = '{0}?executor=2'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.task1])

    def test_filter_by_label(self):
        self.client.force_login(self.user1)
        self.client.post(reverse('tasks:create'), self.task, follow=True)
        created_task = Task.objects.get(name=self.task['name'])
        filtered_list = '{0}?labels=1'.format(reverse('tasks:list'))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(list(response.context['tasks']), [self.task1, created_task])

