"""Forms for labels."""
from django import forms

from .constants import NAME
from .models import Label
from .translations import NAME_TITLE


class LabelForm(forms.ModelForm):
    """Form to create or update label."""

    class Meta:
        model = Label
        fields = [NAME]
        labels = {
            NAME: NAME_TITLE,
        }
