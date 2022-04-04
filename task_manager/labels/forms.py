"""Forms for labels."""
from django import forms
from task_manager.constants import NAME
from task_manager.labels.models import Label
from task_manager.translations import NAME_TITLE


class LabelForm(forms.ModelForm):
    """Form to create or update label."""

    class Meta:
        model = Label
        fields = [NAME]
        labels = {
            NAME: NAME_TITLE,
        }
