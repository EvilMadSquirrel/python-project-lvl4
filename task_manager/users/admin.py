"""Add tasks table to admin site."""
from django.contrib import admin

from .models import User

admin.site.register(User)
