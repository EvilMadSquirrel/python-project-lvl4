from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(null=False)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, null=True, related_name="tasks")
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=False, related_name="tasks")
    executor = models.ForeignKey(User, on_delete=models.PROTECT, null=False, related_name="tasks_in_work")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
