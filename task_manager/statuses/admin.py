"""Add statuses table to admin site."""
from django.contrib import admin

from .models import Status

admin.site.register(Status)
