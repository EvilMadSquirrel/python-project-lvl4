"""Add labels table to admin site."""
from django.contrib import admin

from .models import Label

admin.site.register(Label)
