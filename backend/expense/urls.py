from django.urls import path

from backend.expense import views as v

app_name = 'expense'


urlpatterns = [
    path('', v.expense_list, name='expense_list'),
    path('create/', v.expense_create, name='expense_create'),
    path('expense/paid/', v.expense_paid, name='expense_paid'),
    path('expense/no-paid/', v.expense_no_paid, name='expense_no_paid'),
    path('<int:pk>/', v.expense_detail, name='expense_detail'),
    path('<int:pk>/update/', v.expense_update, name='expense_update'),
    path('<int:pk>/delete/', v.expense_delete, name='expense_delete'),
]
