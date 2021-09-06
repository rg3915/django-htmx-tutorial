from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('backend.core.urls', namespace='core')),
    # path('bookstore/', include('backend.bookstore.urls', namespace='bookstore')),
    # path('expense/', include('backend.expense.urls', namespace='expense')),
    # path('state/', include('backend.state.urls', namespace='state')),
    path('admin/', admin.site.urls),
]
