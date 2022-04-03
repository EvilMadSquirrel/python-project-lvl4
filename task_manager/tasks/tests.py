from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from task_manager.constants import DESCRIPTION, LOGIN_TEST, NAME, TASKS_TEST
from task_manager.labels.constants import LABELS
from task_manager.labels.models import Label
from task_manager.statuses.constants import STATUS
from task_manager.statuses.models import Status
from task_manager.tasks.constants import (
    AUTHOR,
    EXECUTOR,
    TASKS,
    TASKS_CHANGE,
    TASKS_CREATE,
    TASKS_DELETE,
    TASKS_LIST,
)
from task_manager.tasks.models import Task
from task_manager.tasks.translations import (
    BY_ITS_AUTHOR,
    TASK_CHANGED_SUCCESSFULLY,
    TASK_CREATED_SUCCESSFULLY,
    TASK_DELETED_SUCCESSFULLY,
)

STATUS_OK = 200


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
            NAME: "task3",
            DESCRIPTION: "description3",
            STATUS: 1,
            AUTHOR: 1,
            EXECUTOR: 2,
            LABELS: [1, 2],
        }

    def test_tasks_list(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse(TASKS_LIST))
        self.assertEqual(response.status_code, STATUS_OK)
        tasks_list = list(response.context[TASKS])
        self.assertQuerysetEqual(tasks_list, [self.task1, self.task2])

    def test_tasks_list_no_login(self):
        response = self.client.get(reverse(TASKS_LIST))
        self.assertRedirects(response, LOGIN_TEST)

    def test_create_task(self):
        self.client.force_login(self.user1)
        response = self.client.post(
            reverse(TASKS_CREATE),
            self.task,
            follow=True,
        )
        self.assertRedirects(response, TASKS_TEST)
        self.assertContains(response, TASK_CREATED_SUCCESSFULLY)
        created_task = Task.objects.get(name=self.task[NAME])
        self.assertEquals(created_task.name, "task3")

    def test_change_task(self):
        self.client.force_login(self.user1)
        url = reverse(TASKS_CHANGE, args=(self.task1.pk,))
        changed_task = {
            NAME: "changed name",
            DESCRIPTION: "changed description",
            STATUS: 1,
            AUTHOR: 1,
            EXECUTOR: 2,
            LABELS: [3, 4, 5],
        }
        response = self.client.post(url, changed_task, follow=True)
        self.assertRedirects(response, TASKS_TEST)
        self.assertContains(response, TASK_CHANGED_SUCCESSFULLY)
        self.assertEqual(Task.objects.get(pk=self.task1.pk), self.task1)

    def test_delete_task(self):
        self.client.force_login(self.user1)
        url = reverse(TASKS_DELETE, args=(self.task1.pk,))
        response = self.client.post(url, follow=True)
        # noinspection PyTypeChecker
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(pk=self.task1.pk)
        self.assertRedirects(response, TASKS_TEST)
        self.assertContains(response, TASK_DELETED_SUCCESSFULLY)

    def test_delete_task_not_author(self):
        self.client.force_login(self.user1)
        url = reverse(TASKS_DELETE, args=(self.task2.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Task.objects.filter(pk=self.task2.pk).exists())
        self.assertRedirects(response, TASKS_TEST)
        self.assertContains(response, BY_ITS_AUTHOR)

    def test_filter_self_tasks(self):
        self.client.force_login(self.user1)
        filtered_list = "{0}?self_task=on".format(reverse(TASKS_LIST))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertQuerysetEqual(list(response.context[TASKS]), [self.task1])

    def test_filter_by_status(self):
        self.client.force_login(self.user1)
        filtered_list = "{0}?status=2".format(reverse(TASKS_LIST))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertQuerysetEqual(list(response.context[TASKS]), [self.task2])

    def test_filter_by_executor(self):
        self.client.force_login(self.user1)
        filtered_list = "{0}?executor=2".format(reverse(TASKS_LIST))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertQuerysetEqual(list(response.context[TASKS]), [self.task1])

    def test_filter_by_label(self):
        self.client.force_login(self.user1)
        self.client.post(reverse(TASKS_CREATE), self.task, follow=True)
        created_task = Task.objects.get(name=self.task[NAME])
        filtered_list = "{0}?labels=1".format(reverse(TASKS_LIST))
        response = self.client.get(filtered_list)
        self.assertEqual(response.status_code, STATUS_OK)
        self.assertQuerysetEqual(
            list(response.context[TASKS]),
            [self.task1, created_task],
        )
