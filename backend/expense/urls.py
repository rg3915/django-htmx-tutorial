from django.urls import path

from backend.expense import views as v

app_name = 'expense'


urlpatterns = [
    path('', v.expense_list, name='expense_list'),
    path('create/', v.expense_create, name='expense_create'),
]
