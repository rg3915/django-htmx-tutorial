from django.urls import path

from backend.product import views as v

app_name = 'product'


urlpatterns = [
    path('', v.product_list, name='product_list'),
    path('category/<int:pk>/create/', v.category_create, name='category_create'),
    path('<int:product_pk>/category/update/', v.category_update, name='category_update'),  # noqa E501
]
