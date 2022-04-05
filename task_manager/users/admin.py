"""Add tasks table to admin site."""
from django.contrib import admin
from task_manager.users.models import User

admin.site.register(User)
