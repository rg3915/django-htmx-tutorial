from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

# from .forms import BookForm
from .models import Book


class BookListView(ListView):
    model = Book
    paginate_by = 10
