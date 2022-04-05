"""Forms for statuses."""
from django import forms

from .constants import NAME
from .models import Status
from .translations import NAME_TITLE


class StatusForm(forms.ModelForm):
    """Form for create or update status."""

    class Meta:  # Noqa: D106
        model = Status
        fields = [NAME]
        labels = {
            NAME: NAME_TITLE,
        }
