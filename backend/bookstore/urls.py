from django.urls import path

from backend.bookstore import views as v

app_name = 'bookstore'


urlpatterns = [
    path('', v.BookListView.as_view(), name='book_list'),
    path('create/', v.book_create, name='book_create'),
]