from django.db import models

from ..labels.models import Label
from ..statuses.models import Status
from ..users.models import User
from .constants import NAME_MAX_LENGTH, TASKS


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
    labels = models.ManyToManyField(Label, related_name=TASKS, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
