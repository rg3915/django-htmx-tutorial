from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value', 'paid')
    search_fields = ('description',)
    list_filter = ('paid',)

