from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class StatusesListPage(ListView):
    pass

class CreateStatusPage(SuccessMessageMixin,CreateView):
    pass


class ChangeStatusPage(SuccessMessageMixin, UpdateView):
    pass

class DeleteStatusPage(DeleteView):
    pass