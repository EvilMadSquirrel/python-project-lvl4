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
    model = Label
    template_name = "labels_list.html"
    context_object_name = "labels"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Labels")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class CreateLabelPage(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("Label created successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Create label")
        context["button_text"] = _("Create")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class ChangeLabelPage(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = "form.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("Label changed successfully")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Change label")
        context["button_text"] = _("Change")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")


class DeleteLabelPage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = "delete.html"
    success_url = reverse_lazy("labels:list")
    success_message = _("Label deleted successfully")

    def form_valid(self, form):
        if self.get_object().tasks.all():
            messages.error(self.request, _("Cannot delete label because it is in use"))
        else:
            super(DeleteLabelPage, self).form_valid(form)
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Delete label")
        context["button_text"] = _("Yes, delete")
        return context

    def handle_no_permission(self):
        messages.error(self.request, _("You are not authorized"))
        return redirect("login")
