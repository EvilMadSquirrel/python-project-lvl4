from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.
class TasksListPage(ListView):
    pass


class CreateTaskPage(CreateView):
    pass


class ChangeTaskPage(UpdateView):
    pass


class DeleteTaskPage(DeleteView):
    pass
