from django.db import models
from task_manager.constants import NAME_MAX_LENGTH
from task_manager.statuses.translations import STATUSES_TITLE


class Status(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = STATUSES_TITLE
