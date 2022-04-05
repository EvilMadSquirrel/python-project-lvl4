from django.db import models
from task_manager.constants import NAME_MAX_LENGTH
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.constants import TASKS
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, null=False)
    description = models.TextField(null=False)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        null=True,
        related_name=TASKS,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=False,
        related_name=TASKS,
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        related_name="works",
    )
    labels = models.ManyToManyField(Label, related_name=TASKS)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
