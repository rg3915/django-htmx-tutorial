from django.urls import path

from backend.bookstore import views as v

app_name = 'bookstore'


urlpatterns = [
    path('', v.BookListView.as_view(), name='book_list'),
    path('<int:pk>/', v.book_detail, name='book_detail'),
    path('create/', v.book_create, name='book_create'),
    path('<int:pk>/update/', v.book_update, name='book_update'),
    path('<int:pk>/delete/', v.book_delete, name='book_delete'),
    path('<int:pk>/like/', v.book_like, name='book_like'),
    path('<int:pk>/unlike/', v.book_unlike, name='book_unlike'),
]
