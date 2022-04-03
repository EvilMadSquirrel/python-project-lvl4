from django import forms
from task_manager.constants import NAME
from task_manager.labels.models import Label


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = [NAME]
