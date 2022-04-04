"""Forms for statuses."""
from django import forms
from task_manager.constants import NAME
from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm):
    """Form for create or update status."""

    class Meta:  # Noqa: D106
        model = Status
        fields = [NAME]
