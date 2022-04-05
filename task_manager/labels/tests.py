"""Tests for labels."""
from django.test import TestCase
from django.urls import reverse

from ..statuses.models import Status
from ..tasks.models import Task
from .constants import (
    LABELS,
    LABELS_CHANGE,
    LABELS_CREATE,
    LABELS_DELETE,
    LABELS_LIST,
    LABELS_TEST,
    LOGIN_TEST,
    NAME,
)
from .models import Label
from .translations import (
    LABEL_CHANGED_SUCCESSFULLY,
    LABEL_CREATED_SUCCESSFULLY,
    LABEL_DELETED_SUCCESSFULLY,
    LABEL_IN_USE,
)

STATUS_OK = 200

PASSWORD = "111"
TESTUSER = "testuser1"


class TestLabels(TestCase):
    """Tests CRUD for labels."""

    fixtures = ["labels.json", "tasks.json", "users.json", "statuses.json"]

    def setUp(self) -> None:
        """Get data from fixtures."""
        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.label4 = Label.objects.get(pk=4)
        self.label5 = Label.objects.get(pk=5)

        self.status1 = Status.objects.get(pk=1)

        self.task1 = Task.objects.get(pk=1)

    def test_labels_list(self):
        """Check for all labels in labels page."""
        self.client.login(username=TESTUSER, password=PASSWORD)
        response = self.client.get(reverse(LABELS_LIST))
        self.assertEqual(response.status_code, STATUS_OK)
        labels_list = list(response.context[LABELS])
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
        """Check redirect to login page."""
        response = self.client.get(reverse(LABELS_LIST))
        self.assertRedirects(response, LOGIN_TEST)

    def test_create_label(self):
        """Check create new label."""
        self.client.login(username=TESTUSER, password=PASSWORD)
        label = {NAME: "label6"}
        response = self.client.post(reverse(LABELS_CREATE), label, follow=True)
        self.assertRedirects(response, LABELS_TEST)
        self.assertContains(response, LABEL_CREATED_SUCCESSFULLY)
        created_label = Label.objects.get(name=label[NAME])
        self.assertEquals(created_label.name, "label6")

    def test_change_label(self):
        """Check change existing label."""
        self.client.login(username=TESTUSER, password=PASSWORD)
        url = reverse(LABELS_CHANGE, args=(self.label1.pk,))
        new_label = {NAME: "changed"}
        response = self.client.post(url, new_label, follow=True)
        self.assertRedirects(response, LABELS_TEST)
        self.assertContains(response, LABEL_CHANGED_SUCCESSFULLY)
        self.assertEqual(Label.objects.get(pk=self.label1.id), self.label1)

    def test_label_with_tasks_delete(self):
        """Check try to delete label with tasks."""
        self.client.login(username=TESTUSER, password=PASSWORD)
        url = reverse(LABELS_DELETE, args=(self.label1.pk,))
        response = self.client.post(url, follow=True)
        self.assertTrue(Label.objects.filter(pk=self.label1.id).exists())
        self.assertRedirects(response, LABELS_TEST)
        self.assertContains(response, LABEL_IN_USE)

    def test_delete_label(self):
        """Check delete label."""
        self.client.login(username=TESTUSER, password=PASSWORD)
        Task.objects.all().delete()
        url = reverse(LABELS_DELETE, args=(self.label1.pk,))
        response = self.client.post(url, follow=True)
        # noinspection PyTypeChecker
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(pk=self.label1.pk)
        self.assertRedirects(response, LABELS_TEST)
        self.assertContains(response, LABEL_DELETED_SUCCESSFULLY)
