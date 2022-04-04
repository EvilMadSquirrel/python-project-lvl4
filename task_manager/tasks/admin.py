"""Add tasks table to admin site."""
from django.contrib import admin
from task_manager.tasks.models import Task

admin.site.register(Task)
