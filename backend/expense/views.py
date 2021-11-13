from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import ExpenseForm
from .models import Expense


def expense_list(request):
    template_name = 'expense/expense_list.html'
    form = ExpenseForm(request.POST or None)

    expenses = Expense.objects.all()

    context = {'object_list': expenses, 'form': form}
    return render(request, template_name, context)


@require_http_methods(['POST'])
def expense_create(request):
    form = ExpenseForm(request.POST or None)

    if form.is_valid():
        expense = form.save()

    context = {'object': expense}
    return render(request, 'expense/hx/expense_hx.html', context)


@require_http_methods(['POST'])
def expense_paid(request):
    ids = request.POST.getlist('ids')

    # Edita as despesas selecionadas.
    Expense.objects.filter(id__in=ids).update(paid=True)

    # Retorna todas as despesas novamente.
    expenses = Expense.objects.all()

    context = {'object_list': expenses}
    return render(request, 'expense/expense_table.html', context)


@require_http_methods(['POST'])
def expense_no_paid(request):
    ids = request.POST.getlist('ids')

    # Edita as despesas selecionadas.
    Expense.objects.filter(id__in=ids).update(paid=False)

    # Retorna todas as despesas novamente.
    expenses = Expense.objects.all()

    context = {'object_list': expenses}
    return render(request, 'expense/expense_table.html', context)


def expense_detail(request, pk):
    template_name = 'expense/hx/expense_detail.html'
    obj = Expense.objects.get(pk=pk)
    form = ExpenseForm(request.POST or None, instance=obj)

    context = {'object': obj, 'form': form}
    return render(request, template_name, context)


def expense_update(request, pk):
    template_name = 'expense/hx/expense_hx.html'
    obj = Expense.objects.get(pk=pk)
    form = ExpenseForm(request.POST or None, instance=obj)
    context = {'object': obj}

    if request.method == 'POST':
        if form.is_valid():
            form.save()

    return render(request, template_name, context)
