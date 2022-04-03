from django import forms
from task_manager.constants import NAME
from task_manager.statuses.models import Status


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = [NAME]
