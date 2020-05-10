from django.views import generic
from .models import Category, Book
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

class IndexView(generic.ListView):
    model = Book

class DetailView(generic.DetailView):
    model = Book

class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Book
    #fields = '__all__'
    fields = ['name', 'books_author', 'publisher', 'category', 'review']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Book
    #fields = '__all__'
    fields = ['name', 'books_author', 'publisher', 'category', 'review']

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Book
    success_url = reverse_lazy('bookreview:index')