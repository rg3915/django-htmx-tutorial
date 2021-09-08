from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('backend.core.urls', namespace='core')),
    path('expense/', include('backend.expense.urls', namespace='expense')),
    path('bookstore/', include('backend.bookstore.urls', namespace='bookstore')),
    path('state/', include('backend.state.urls', namespace='state')),
    path('product/', include('backend.product.urls', namespace='product')),
    path('admin/', admin.site.urls),
]
