import django_filters
from django import forms
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.utils.translation import gettext as _
from task_manager.constants import DESCRIPTION, ID, NAME
from task_manager.labels.constants import LABELS
from task_manager.labels.models import Label
from task_manager.statuses.constants import STATUS
from task_manager.tasks.constants import EXECUTOR
from task_manager.tasks.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [NAME, DESCRIPTION, STATUS, EXECUTOR, LABELS]


class TasksFilter(django_filters.FilterSet):
    all_labels = Label.objects.values_list(ID, NAME, named=True).all()
    labels = django_filters.filters.ChoiceFilter(
        label=_("Label"),
        choices=all_labels,
    )
    all_executors = User.objects.values_list(
        ID,
        Concat("first_name", Value(" "), "last_name"),
        named=True,
    ).all()
    executor = django_filters.filters.ChoiceFilter(
        label=_("Executor"), choices=all_executors,
    )
    self_task = django_filters.filters.BooleanFilter(
        label=_("Only my tasks"),
        widget=forms.CheckboxInput(),
        method="filter_self",
        field_name="self_task",
    )

    def filter_self(self, queryset, name, value):
        if value:
            author = getattr(self.request, "user", None)
            queryset = queryset.filter(author=author)
        return queryset

    class Meta:
        model = Task
        fields = [STATUS, EXECUTOR, LABELS]
