"""Add tasks table to admin site."""
from django.contrib import admin

from .models import Task

admin.site.register(Task)
