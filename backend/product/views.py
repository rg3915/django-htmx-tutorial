from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Category, Product


def product_list(request):
    template_name = 'product/product_list.html'
    object_list = Product.objects.all()
    categories = Category.objects.all()

    context = {
        'object_list': object_list,
        'categories': categories,
    }
    return render(request, template_name, context)


def category_create(request, pk):
    template_name = 'product/hx/category_modal_form_hx.html'
    product = Product.objects.get(pk=pk)

    if request.method == 'POST':
        title = request.POST.get('categoria')
        # Cria a nova categoria
        category = Category.objects.create(title=title)

        # Associa a nova categoria ao produto atual.
        product.category = category
        product.save()

        template_name = 'product/hx/product_result_hx.html'

        categories = Category.objects.all()
        context = {
            'object': product,
            'categories': categories,
        }
        return render(request, template_name, context)

    context = {'object': product}
    return render(request, template_name, context)


@require_http_methods(['POST'])
def category_update(request, product_pk):
    product = Product.objects.get(pk=product_pk)

    category_pk = request.POST.get('category')
    category = Category.objects.get(pk=category_pk)

    product.category = category
    product.save()
    return HttpResponse('ok')
