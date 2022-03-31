from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Label
from .forms import LabelForm


class LabelsListPage(LoginRequiredMixin, ListView):
    pass


class CreateLabelPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    pass


class ChangeLabelPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    pass


class DeleteLabelPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    pass
