"""Forms for tasks."""
import django_filters
from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _
from task_manager.constants import DESCRIPTION, ID, NAME
from task_manager.labels.constants import LABELS
from task_manager.labels.models import Label
from task_manager.labels.translations import LABEL_TITLE, LABELS_TITLE
from task_manager.statuses.constants import STATUS
from task_manager.statuses.models import Status
from task_manager.tasks.constants import EXECUTOR
from task_manager.tasks.models import Task
from task_manager.tasks.translations import (
    DESCRIPTION_LABEL,
    EXECUTOR_LABEL,
    MY_TASKS,
    STATUS_LABEL,
)
from task_manager.translations import NAME_TITLE
from task_manager.users.constants import FIRST_NAME, LAST_NAME
from task_manager.users.models import User


class TaskForm(forms.ModelForm):
    """Form to create or update task."""

    class Meta:
        model = Task
        fields = [NAME, DESCRIPTION, STATUS, EXECUTOR, LABELS]
        labels = {
            NAME: NAME_TITLE,
            DESCRIPTION: DESCRIPTION_LABEL,
            STATUS: STATUS_LABEL,
            EXECUTOR: EXECUTOR_LABEL,
            LABELS: LABELS_TITLE,
        }


class TasksFilter(django_filters.FilterSet):
    """Filter set for tasks."""

    all_statuses = Status.objects.values_list(ID, NAME, named=True).all()
    status = django_filters.filters.ChoiceFilter(
        label=STATUS_LABEL,
        choices=all_statuses,
    )

    all_labels = Label.objects.values_list(ID, NAME, named=True).all()
    labels = django_filters.filters.ChoiceFilter(
        label=LABEL_TITLE,
        choices=all_labels,
    )
    all_executors = User.objects.values_list(
        ID,
        Concat(FIRST_NAME, Value(" "), LAST_NAME),
        named=True,
    ).all()
    executor = django_filters.filters.ChoiceFilter(
        label=_(EXECUTOR_LABEL),
        choices=all_executors,
    )
    self_task = django_filters.filters.BooleanFilter(
        label=MY_TASKS,
        widget=forms.CheckboxInput(),
        method="filter_self",
        field_name="self_task",
    )

    def filter_self(self, queryset, name, value):
        """If filter is selected returns queryset of current user tasks.

        Args:
            queryset: Queryset which was created by other filters before.
            name(str): Filter's name.
            value(bool): Filter's value.

        Returns:
            Queryset.
        """
        if value:
            author = getattr(self.request, "user", None)
            queryset = queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = [STATUS, EXECUTOR, LABELS]
