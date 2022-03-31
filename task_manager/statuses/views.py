from django.contrib import messages
from django.shortcuts import redirect
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

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class CreateStatusPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create status")
        context["button_text"] = _("Create")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class ChangeStatusPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = "form.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status changed successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Change status")
        context["button_text"] = _("Change")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class DeleteStatusPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = "delete.html"
    success_url = reverse_lazy("statuses:list")
    success_message = _("Status deleted successfully")

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, _("Cannot delete status because it is in use"))
        else:
            super(DeleteStatusPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete status")
        context["button_text"] = _("Delete")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")
