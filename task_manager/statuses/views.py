from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from .models import Status
from .forms import StatusForm


class StatusesListPage(LoginRequiredMixin, ListView):
    model = Status
    template_name = "statuses_list.html"
    context_object_name = "statuses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Statuses")
        return context


class CreateStatusPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status created successfully.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create status")
        context["button_text"] = _("Create")
        return context


class ChangeStatusPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status changed successfully.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Change status")
        context["button_text"] = _("Change")
        return context


class DeleteStatusPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status deleted successfully.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete status")
        context["button_text"] = _("Delete")
        return context
