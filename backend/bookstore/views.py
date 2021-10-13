from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from .forms import BookForm
from .models import Book


class BookListView(ListView):
    model = Book
    paginate_by = 10


def book_detail(request, pk):
    template_name = 'bookstore/hx/book_detail_hx.html'
    obj = Book.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)


def book_create(request):
    template_name = 'bookstore/hx/book_form_hx.html'
    form = BookForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            book = form.save()
            template_name = 'bookstore/hx/book_result_hx.html'
            context = {'object': book}
            return render(request, template_name, context)

    context = {'form': form}
    return render(request, template_name, context)


def book_update(request, pk):
    template_name = 'bookstore/hx/book_update_form_hx.html'
    instance = Book.objects.get(pk=pk)
    form = BookForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            book = form.save()
            template_name = 'bookstore/hx/book_result_hx.html'
            context = {'object': book}
            return render(request, template_name, context)

    context = {'form': form, 'object': instance}
    return render(request, template_name, context)


@require_http_methods(['DELETE'])
def book_delete(request, pk):
    template_name = 'bookstore/book_table.html'
    obj = Book.objects.get(pk=pk)
    obj.delete()
    return render(request, template_name)


@require_http_methods(['POST'])
def book_like(request, pk):
    template_name = 'bookstore/hx/book_result_hx.html'
    book = Book.objects.get(pk=pk)
    book.like = True
    book.save()
    context = {'object': book}
    return render(request, template_name, context)


@require_http_methods(['POST'])
def book_unlike(request, pk):
    template_name = 'bookstore/hx/book_result_hx.html'
    book = Book.objects.get(pk=pk)
    book.like = False
    book.save()
    context = {'object': book}
    return render(request, template_name, context)
