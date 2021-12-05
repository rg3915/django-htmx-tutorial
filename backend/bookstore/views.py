from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from .forms import BookForm
from .models import Book


class BookListView(ListView):
    model = Book
    paginate_by = 10


def book_create(request):
    template_name = 'bookstore/book_form.html'
    form = BookForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            book = form.save()
            template_name = 'bookstore/hx/book_result_hx.html'
            context = {'object': book}
            return render(request, template_name, context)

    context = {'form': form}
    return render(request, template_name, context)
