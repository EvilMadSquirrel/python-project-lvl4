from django.db import models
from task_manager.constants import NAME_MAX_LENGTH


class Label(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
