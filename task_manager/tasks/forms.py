"""Forms for tasks."""
import django_filters
from django import forms
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _

from ..labels.models import Label
from ..statuses.models import Status
from ..users.models import User
from .constants import (
    DESCRIPTION,
    EXECUTOR,
    FIRST_NAME,
    ID,
    LABELS,
    LAST_NAME,
    NAME,
    STATUS,
)
from .models import Task
from .translations import (
    DESCRIPTION_LABEL,
    EXECUTOR_LABEL,
    LABEL_TITLE,
    LABELS_TITLE,
    MY_TASKS,
    NAME_TITLE,
    STATUS_LABEL,
)


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
