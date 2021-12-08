# django-htmx-tutorial

Tutorial sobre como trabalhar com [Django](https://www.djangoproject.com/) e [htmx](https://htmx.org/).

![htmx.png](img/htmx.png)

## Este projeto foi feito com:

* [Python 3.9.6](https://www.python.org/)
* [Django 3.2.*](https://www.djangoproject.com/)
* [htmx](https://htmx.org/)

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-htmx-tutorial.git
cd django-htmx-tutorial
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
python manage.py runserver
```

## Exemplos

* [Filtrar várias tabelas com um clique](#filtrar-v%C3%A1rias-tabelas-com-um-clique)

<img src="img/a03_tabela.png" alt="" width="200px">


* [Filtrar com dropdowns dependentes](#filtrar-com-dropdowns-dependentes)

<img src="img/a02_combobox.png" alt="" width="200px">


* [Adicionar itens](#adicionar-itens)

<img src="img/01_expense_add.png" alt="" width="200px">


* [Pagar (editar) vários itens (Bulk Update)](#pagar-editar-vários-itens-bulk-update)

<img src="img/02_expense_bulk_update.png" alt="" width="200px">


* [Editar um item](#editar-um-item)

<img src="img/03_expense_update.png" alt="" width="200px">


* [Deletar um item](#deletar-um-item)

<img src="img/04_expense_delete.png" alt="" width="200px">


* [client-side-templates](#client-side-templates)

* [Bookstore (modal)](#bookstore)

* [Like e unlike](#like-e-unlike)

* [Criar categoria](#criar-uma-nova-categoria)

* [Trocar de categoria](#trocar-a-categoria)


## Passo a passo

### Clonando o projeto base

```
git clone https://github.com/rg3915/django-htmx-tutorial.git
cd django-htmx-tutorial
git checkout passo-a-passo

python -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
pip install ipdb

python contrib/env_gen.py

python manage.py migrate
python manage.py createsuperuser --username="admin" --email=""
```

Vamos editar:

* base.html
* nav.html
* index.html


Em `base.html` escreva

```html
<!-- HTMX -->
<script src="https://unpkg.com/htmx.org@1.6.0"></script>
<script src="https://unpkg.com/htmx.org@1.6.0/dist/ext/client-side-templates.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mustache@4.2.0/mustache.min.js"></script>
```

Em `nav.html` escreva

```html
<li class="nav-item">
  <a class="nav-link" href="{% url 'state:state_list' %}">Estados</a>
</li>
<li class="nav-item">
  <a class="nav-link" href="{ url 'expense:expense_list' %}">Despesas</a>
</li>
<li class="nav-item">
  <a class="nav-link" href="{ url 'expense:expense_client' %}">Despesas (Client side)</a>
</li>
```

Corrija o link em `index.html`

```html
<a href="{% url 'state:state_list' %}">Estados</a>
```


## Exemplos

### Filtrar várias tabelas com um clique

![a03_tabela.png](img/a03_tabela.png)

Considere a app `state`.


Vamos editar:

* views.py
* urls.py
* state_list.html
* hx/state_hx.html


Em `state/views.py` escreva

```python
# state/views.py
from django.shortcuts import render

from .states import states


def state_list(request):
    template_name = 'state/state_list.html'

    regions = (
        ('n', 'Norte'),
        ('ne', 'Nordeste'),
        ('s', 'Sul'),
        ('se', 'Sudeste'),
        ('co', 'Centro-Oeste'),
    )

    context = {'regions': regions}
    return render(request, template_name, context)
```

Em `state/urls.py` escreva

```python
# state/urls.py
from django.urls import path

from backend.state import views as v

app_name = 'state'


urlpatterns = [
    path('', v.state_list, name='state_list'),
    path('result/', v.state_result, name='state_result'),
]

```

Crie as pastas

```
mkdir -p state/templates/state/hx
```


Escreva o template

`touch state/templates/state/state_list.html`

```html
<!-- state/templates/state/state_list.html -->
{% extends "base.html" %}

{% block content %}
<h1>Regiões e Estados do Brasil</h1>

<h2 style="color: #3465a4;">Filtrando várias tabelas com um clique</h2>

<div class="row">

  <div class="col">
    <table class="table table-hover">
      <thead>
        <tr>
          <th>Região</th>
        </tr>
      </thead>
      <tbody>
        {% for region in regions %}
        <tr
          hx-get="{% url 'state:state_result' %}?region={{region.0}}"
          hx-target="#states"
        >
          <td>
            <a>{{ region.1 }}</a>
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <div class="col">
    <table class="table">
      <thead>
        <tr>
          <th>Estados</th>
        </tr>
      </thead>
      <tbody id="states">
        <!-- O novo conteúdo será inserido aqui. -->
      </tbody>
    </table>
  </div>

</div>
{% endblock content %}
```

Em `state/views.py` escreva

```python
# state/views.py
def get_states(region):
    return [state for state in states.get(region).items()]

def state_result(request):
    template_name = 'state/hx/state_hx.html'
    region = request.GET.get('region')

    ufs = {
        'n': get_states('Norte'),
        'ne': get_states('Nordeste'),
        's': get_states('Sul'),
        'se': get_states('Sudeste'),
        'co': get_states('Centro-Oeste'),
    }

    context = {'ufs': ufs[region]}
    return render(request, template_name, context)
```

Escreva o template

`touch state/templates/state/hx/state_hx.html`

```html
<!-- state/templates/state/hx/state_hx.html -->
{% for uf in ufs %}
  <tr>
    <td>{{ uf.1 }}</td>
  </tr>
{% endfor %}
```

Descomente em `urls.py`

```
path('state/', include('backend.state.urls', namespace='state')),
```


---

### Filtrar com dropdowns dependentes

![a02_combobox.png](img/a02_combobox.png)

Vamos editar:

* urls.py
* views.py
* hx/uf_hx.html
* state_list.html


Edite `state/urls.py`

```python
# state/urls.py
...
path('uf/', v.uf_list, name='uf_list'),
...
```

Edite `state/views.py`

```python
# state/views.py
def uf_list(request):
    template_name = 'state/hx/uf_hx.html'
    region = request.GET.get('region')

    ufs = {
        'n': get_states('Norte'),
        'ne': get_states('Nordeste'),
        's': get_states('Sul'),
        'se': get_states('Sudeste'),
        'co': get_states('Centro-Oeste'),
    }

    context = {'ufs': ufs[region]}
    return render(request, template_name, context)
```

Edite

`touch state/templates/state/hx/uf_hx.html`

```html
<!-- state/templates/state/hx/uf_hx.html -->
{% for uf in ufs %}
  <option value="{{ uf.0 }}">{{ uf.1 }}</option>
{% endfor %}
```

Edite `state/templates/state/state_list.html`

```html
<h2 style="color: #3465a4;">Filtro com dropdowns dependentes</h2>

<div class="row">

  <div class="col">
    <label>Região</label>
    <select
      name="region"
      class="form-control"
      hx-get="{% url 'state:uf_list' %}"
      hx-target="#uf"
    >
      <option value="">-----</option>
      {% for region in regions %}
        <option value="{{ region.0 }}">{{ region.1 }}</option>
      {% endfor %}
    </select>
  </div>

  <div class="col">
    <label>UF</label>
    <select
      id="uf"
      class="form-control"
    >
      <option value="">-----</option>
      <!-- O novo conteúdo será inserido aqui. -->
    </select>
  </div>

</div>

<hr>

...
```

---

### A base para despesas

Considere o desenho a seguir:

![expense_base.png](img/expense_base.png)

`expense_hx.html` será inserido em
`expense_table.hmtl`, que por sua vez
será inserido em `expense_list.html`.

Sendo que `expense_hx.html` será repetido várias vezes por causa do laço de repetição em `expense_table.hmtl`.

---

### Adicionar itens

![01_expense_add.png](img/01_expense_add.png)

Vamos editar:

* models.py
* admin.py
* forms.py
* views.py
* urls.py
* expense_list.html
* expense_table.html
* hx/expense_hx.html
* nav.html
* index.html


Escreva o `expense/models.py`

```python
# expense/models.py
from django.db import models

from backend.core.models import TimeStampedModel


class Expense(TimeStampedModel):
    description = models.CharField('descrição', max_length=30)
    value = models.DecimalField('valor', max_digits=7, decimal_places=2)
    paid = models.BooleanField('pago', default=False)

    class Meta:
        ordering = ('description',)
        verbose_name = 'despesa'
        verbose_name_plural = 'despesas'

    def __str__(self):
        return self.description
```

Escreva o `expense/admin.py`

```python
# expense/admin.py
from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value', 'paid')
    search_fields = ('description',)
    list_filter = ('paid',)
```

Escreva 

`touch expense/forms.py`

```python
# expense/forms.py
from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Expense
        fields = ('description', 'value')
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Descrição', 'autofocus': True}),
            'value': forms.NumberInput(attrs={'placeholder': 'Valor'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
```

Escreva o `expense/views.py`

```python
# expense/views.py
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
```

Escreva o `expense/urls.py`

```python
# expense/urls.py
from django.urls import path

from backend.expense import views as v

app_name = 'expense'


urlpatterns = [
    path('', v.expense_list, name='expense_list'),
    path('create/', v.expense_create, name='expense_create'),
]
```

Crie as pastas

```
mkdir -p expense/templates/expense
```


Escreva

`touch expense/templates/expense/expense_list.html`


```html
<!-- expense_list.html -->
{% extends "base.html" %}

{% block content %}
<h1>Lista de Despesas</h1>
<div class="row">
  <div class="col">
    <form
      class="form-inline p-3"
      hx-post="{% url 'expense:expense_create' %}"
      hx-target="#expenseTbody"
      hx-indicator=".htmx-indicator"
      hx-swap="afterbegin"
    >
      {% csrf_token %}
      {% for field in form %}
      <div class="form-group p-2">
        {{ field }}
        {{ field.errors }}
        {% if field.help_text %}
        <small class="text-muted">{{ field.help_text|safe }}</small>
        {% endif %}
      </div>
      {% endfor %}
      <div class="form-group">
        <button
          type="submit"
          class="btn btn-primary ml-2"
        >Adicionar</button>
      </div>
    </form>
  </div>
</div>

<div
  id="checkedExpenses"
  class="col pt-2"
>
  <form>
    <table class="table">
      <thead>
        <tr>
          <th></th>
          <th>Descrição</th>
          <th>Valor</th>
          <th class="text-center">Pago</th>
          <th class="text-center">Ações</th>
        </tr>
      </thead>
      <tbody id="expenseTbody">
        {% include "./expense_table.html" %}
      </tbody>
    </table>
  </form>
</div>

{% endblock content %}

{% block js %}
<script>
document.body.addEventListener('htmx:configRequest', (event) => {
  event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});
</script>
{% endblock js %}
```

Escreva

`touch expense/templates/expense/expense_table.html`

```html
<!-- expense_table.html -->
{% for object in object_list %}
  {% include "./hx/expense_hx.html" %}
{% endfor %}
```

Escreva

`touch expense/templates/expense/hx/expense_hx.html`

```html
<!-- hx/expense_hx.html -->
<tr
  hx-target="this"
  hx-swap="outerHTML"
  class="person {% if object.paid %}activate{% else %}deactivate{% endif %}"
>
  <td>
    <input
      type="checkbox"
      name="ids"
      value="{{ object.pk }}"
    >
  </td>
  <td>{{ object.description }}</td>
  <td>{{ object.value }}</td>
  <td class="text-center">
    {% if object.paid %}
    <span>
      <i class="fa fa-check-circle ok"></i>
    </span>
    {% else %}
    <span>
      <i class="fa fa-times-circle no"></i>
    </span>
    {% endif %}
  </td>
</tr>
```

Edite `nav.html`

```html
<a class="nav-link" href="{% url 'expense:expense_list' %}">Despesas</a>
```

Edite `index.html`

```html
<p><a href="{% url 'expense:expense_list' %}">Despesas</a> CRUD com SPA</p>
```

Descomente `urls.py`

```python
path('expense/', include('backend.expense.urls', namespace='expense')),
```


---

### Pagar (editar) vários itens (Bulk Update)

![02_expense_bulk_update.png](img/02_expense_bulk_update.png)

Vamos editar:

* views.py
* urls.py
* expense_list.html


Escreva o `expense/views.py`

```python
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
```

Escreva o `expense/urls.py`

```python
path('expense/paid/', v.expense_paid, name='expense_paid'),
path('expense/no-paid/', v.expense_no_paid, name='expense_no_paid'),
```

Escreva o `expense/expense_list.html`

```html
<!-- expense_list.html -->
<div
  class="col"
  hx-include="#checkedExpenses"
  hx-target="#expenseTbody"
>
  <a
    class="btn btn-outline-success"
    hx-post="{% url 'expense:expense_paid' %}"
  >Pago</a>
  <a
    class="btn btn-outline-danger"
    hx-post="{% url 'expense:expense_no_paid' %}"
  >Não Pago</a>
  <span class="lead"><strong>Bulk update</strong></span>
</div>
```

---

### Editar um item

![03_expense_update.png](img/03_expense_update.png)

Vamos editar:

* views.py
* urls.py
* hx/expense_hx.html
* hx/expense_detail.html


Escreva o `expense/views.py`

```python
# expense/views.py
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
```


Escreva o `expense/urls.py`

```python
# expense/urls.py
path('<int:pk>/', v.expense_detail, name='expense_detail'),
path('<int:pk>/update/', v.expense_update, name='expense_update'),
```

Escreva o `expense/hx/expense_hx.html`

```html
<!-- expense/hx/expense_hx.html -->
<td class="text-center">
    <span hx-get="{% url 'expense:expense_detail' object.pk %}">
      <i class="fa fa-pencil-square-o link span-is-link"></i>
    </span>
  </td>
```


Escreva

`touch expense/templates/expense/hx/expense_detail.html`

```html
<!-- expense_detail.html -->
<tr id="trExpense">
  <td></td>
  <td>{{ form.description }}</td>
  <td>{{ form.value }}</td>
  <td></td>
  <td class="text-center">
    <button
      type="submit"
      class="btn btn-success"
      hx-post="{% url 'expense:expense_update' object.pk %}"
      hx-target="#trExpense"
      hx-swap="outerHTML"
    >
      OK
    </button>
    <button
      class="btn btn-danger"
      hx-get="{% url 'expense:expense_update' object.pk %}"
      hx-target="#trExpense"
      hx-swap="outerHTML"
    >
      <i class="fa fa-close"></i>
    </button>
  </td>
</tr>
```

---

### Deletar um item

![04_expense_delete.png](img/04_expense_delete.png)

Vamos editar:

* views.py
* urls.py
* hx/expense_hx.html


Escreva o `expense/views.py`

```python
# expense/views.py
@require_http_methods(['DELETE'])
def expense_delete(request, pk):
    obj = Expense.objects.get(pk=pk)
    obj.delete()
    return render(request, 'expense/expense_table.html')
```

Escreva o `expense/urls.py`

```python
# expense/urls.py
path('<int:pk>/delete/', v.expense_delete, name='expense_delete'),
```

Escreva o `expense/hx/expense_hx.html`

```html
<!-- expense/hx/expense_hx.html -->
<td class="text-center">
    ...
    <span
      hx-delete="{% url 'expense:expense_delete' object.pk %}"
      hx-confirm="Deseja mesmo deletar?"
      hx-target="closest tr"
      hx-swap="outerHTML swap:500ms"
    >
      <i class="fa fa-trash no span-is-link pl-2"></i>
    </span>
  </td>
```

---

### client-side-templates

https://htmx.org/extensions/client-side-templates/

Vamos editar:


```python
# expense/models.py

class Expense(TimeStampedModel):
    ...
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'value': self.value,
            'paid': self.paid,
        }
```

Escreva o `expense/views.py`

```python
# expense/views.py
def expense_json(self):
    expenses = Expense.objects.all()
    data = [expense.to_dict() for expense in expenses]
    return JsonResponse({'data': data})


def expense_client(request):
    template_name = 'expense/expense_client.html'
    return render(request, template_name)
```

Escreva o `expense/urls.py`

```python
# expense/urls.py
...
path('json/', v.expense_json, name='expense_json'),
path('client/', v.expense_client, name='expense_client'),
```

Escreva

`touch expense/templates/expense/expense_client.html`

```html
<!-- expense_client.html -->
{% extends "base.html" %}

{% block content %}
<h1>Lista de Despesas (Client side)</h1>
<h3>Consumindo API Rest</h3>

<div hx-ext="client-side-templates">
  <button
    class="btn btn-primary"
    hx-get="{% url 'expense:expense_json' %}"
    hx-swap="innerHTML"
    hx-target="#content"
    mustache-template="foo"
  >
    Clique para carregar os dados
  </button>

  <table class="table">
    <thead>
      <tr>
        <th>Descrição</th>
        <th>Valor</th>
        <th class="text-center">Pago</th>
      </tr>
    </thead>
    <tbody id="content">
    </tbody>
    <template id="foo">
      <!-- Mustache looping -->
      { #data }
      <tr>
        <td>{ description }</td>
        <td>{ value }</td>
        <td class="text-center">
          <!-- Mustache conditional -->
          <!-- http://mustache.github.io/mustache.5.html#Inverted-Sections -->
          { #paid } <i class="fa fa-check-circle ok"></i> { /paid }
          { ^paid } <i class="fa fa-times-circle no"></i> { /paid }
        </td>
      </tr>
      { /data }
    </template>

  </table>
</div>

{% endblock content %}

{% block js %}
<script>
  // https://github.com/janl/mustache.js/#custom-delimiters
  Mustache.tags = ['{', '}'];
</script>
{% endblock js %}
```

Edite `nav.html`

```html
<a class="nav-link" href="{% url 'expense:expense_client' %}">Despesas (Client side)</a>
```

**Atenção:** tentar resolver o problema de [cors-headers](https://github.com/adamchainz/django-cors-headers).


### Json Server

#### Instalação

```
npm install -g json-server
```

Crie um `db.json`

```
{
  "expenses": {
    "data": [
      { "description": "Lanche", "value": 20, "paid": true },
      { "description": "Conta de luz", "value": 80, "paid": false },
      { "description": "Refrigerante", "value": 5.5, "paid": true }
    ]
  }
}
```

#### Server

```
json-server --watch db.json
```

Na pasta principal, escreva

`touch index.html`

Mude o endpoint para `http://localhost:3000/expenses`

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
  <link rel="shortcut icon" href="https://www.djangoproject.com/favicon.ico">
  <title>htmx</title>

  <!-- Bootstrap core CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">

  <!-- Font-awesome -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">

  <!-- HTMX -->
  <script src="https://unpkg.com/htmx.org@1.6.0"></script>
  <script src="https://unpkg.com/htmx.org@1.6.0/dist/ext/client-side-templates.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/mustache@4.2.0/mustache.min.js"></script>

  <style>
    .no {
      color: red;
    }
    .ok {
      color: green;
    }
  </style>
</head>
<body>
  <h1>Lista de Despesas (Client side)</h1>
<h3>Consumindo API Rest</h3>

<div hx-ext="client-side-templates">
  <!-- http://localhost:8000/expense/json/ -->
  <button
    class="btn btn-primary"
    hx-get="http://localhost:3000/expenses"
    hx-swap="innerHTML"
    hx-target="#content"
    mustache-template="foo"
  >
    Clique para carregar os dados
  </button>

  <table class="table">
    <thead>
      <tr>
        <th>Descrição</th>
        <th>Valor</th>
        <th class="text-center">Pago</th>
      </tr>
    </thead>
    <tbody id="content">
    </tbody>
    <template id="foo">
      <!-- Mustache looping -->
      {{ #data }}
      <tr>
        <td>{{ description }}</td>
        <td>{{ value }}</td>
        <td class="text-center">
          <!-- Mustache conditional -->
          <!-- http://mustache.github.io/mustache.5.html#Inverted-Sections -->
          {{ #paid }} <i class="fa fa-check-circle ok"></i> {{ /paid }}
          {{ ^paid }} <i class="fa fa-times-circle no"></i> {{ /paid }}
        </td>
      </tr>
      {{ /data }}
    </template>

  </table>
</div>
</body>
</html>
```

---

## Bookstore

Veremos um exemplo do uso de Bootstrap modal com htmx.

```
cd backend
python ../manage.py startapp bookstore
```

Vamos editar:

* nav.html
* settings.py
* urls.py
* bookstore/apps.py
* bookstore/views.py
* bookstore/models.py
* bookstore/admin.py
* bookstore/urls.py
* bookstore/templates/bookstore/book_list.html
* bookstore/templates/bookstore/book_table.html
* bookstore/templates/bookstore/hx/book_result_hx.html


Edite `nav.html`

```html
<li class="nav-item">
  <a class="nav-link" href="{% url 'bookstore:book_list' %}">Livros (Modal)</a>
</li>
```

Edite `settings.py`

```python
INSTALLED_APPS = [
    ...
    'backend.bookstore',
    ...
]
```


Edite `urls.py`


```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    ...
    path('bookstore/', include('backend.bookstore.urls', namespace='bookstore')),
    ...
]
```


Edite `bookstore/apps.py`

```python
from django.apps import AppConfig


class BookstoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.bookstore'
```

Edite `bookstore/views.py`

```python
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

# from .forms import BookForm
from .models import Book


class BookListView(ListView):
    model = Book
    paginate_by = 10
```


Edite `bookstore/models.py`

```python
from django.db import models
from django.urls import reverse_lazy


class Book(models.Model):
    title = models.CharField('título', max_length=100, unique=True)
    author = models.CharField('autor', max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'livro'
        verbose_name_plural = 'livros'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('bookstore:book_detail', kwargs={'pk': self.pk})
```


Edite `bookstore/admin.py`

```python
from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author')
```


Edite `bookstore/urls.py`

```python
from django.urls import path

from backend.bookstore import views as v

app_name = 'bookstore'


urlpatterns = [
    path('', v.BookListView.as_view(), name='book_list'),
]
```


```
mkdir -p backend/bookstore/templates/bookstore/includes
```

```html
cat << EOF > backend/bookstore/templates/bookstore/book_list.html
<!-- book_list.html -->
{% extends "base.html" %}

{% block content %}
<div>
  <div class="row">
    <div class="col-auto">
      <h1>Lista de Livros</h1>
    </div>
    <div class="col-auto">
      <a href="" class="btn btn-primary">Adicionar</a>
    </div>
  </div>
  <table class="table">
    <thead>
      <tr>
        <th>Título</th>
        <th>Autor</th>
        <th>Ações</th>
      </tr>
    </thead>
    <tbody id="bookTbody">
      {% include "./book_table.html" %}
    </tbody>
  </table>
</div>
{% endblock content %}
EOF
```

```html
cat << EOF > backend/bookstore/templates/bookstore/book_table.html
<!-- book_table.html -->
{% for object in object_list %}
  {% include "./hx/book_result_hx.html" %}
{% endfor %}
EOF
```

```html
cat << EOF > backend/bookstore/templates/bookstore/hx/book_result_hx.html
<!-- hx/book_result_hx.html -->
<tr id="trBook{{ object.pk }}">
  <td>
    <a href="">{{ object.title }}</a>
  </td>
  <td>{{ object.author|default:'---' }}</td>
  <td></td>
</tr>
EOF
```

## Adicionar

Vamos editar:

* bookstore/views.py
* bookstore/urls.py
* bookstore/forms.py
* bookstore/templates/bookstore/book_list.html
* bookstore/templates/bookstore/includes/add_modal.html


Edite `bookstore/views.py`


```python
...
from .forms import BookForm
from .models import Book


def book_create(request):
    template_name = 'bookstore/hx/book_form_hx.html'
    form = BookForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            book = form.save()
            template_name = 'bookstore/hx/book_result_hx.html'
            context = {'object': book}
            return render(request, template_name, context)

    context = {'form': form}
    return render(request, template_name, context)

```


Edite `bookstore/urls.py`

```python
...
path('create/', v.book_create, name='book_create'),
...
```

```python
cat << EOF > backend/bookstore/forms.py
from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Book
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
EOF
```

Edite `backend/bookstore/templates/bookstore/book_list.html`

```html
<!-- book_list.html -->

<a
  href=""
  class="btn btn-primary"
  data-toggle="modal"
  data-target="#addModal"
  hx-get="{% url 'bookstore:book_create' %}"
  hx-target="#addContent"
  hx-swap="innerHTML"
>Adicionar</a>
...

{% include "./includes/add_modal.html" %}

{% endblock content %}

```


```html
cat << EOF > backend/bookstore/templates/bookstore/includes/add_modal.html
<!-- addModal -->
<div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="addModalLabel">
  <div class="modal-dialog" role="document">
    <div id="addContent" class="modal-content">
      <!-- O novo conteúdo será inserido aqui. -->
      <div class="modal-header">
        <h4 class="modal-title" id="detailModalLabel">Modal title</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
        <button type="submit" class="btn btn-primary">Salvar</button>
      </div>
    </div>
  </div>
</div>
EOF

```

```html
cat << EOF > backend/bookstore/templates/bookstore/hx/book_form_hx.html
<!-- book_form_hx.html -->
<div class="modal-header">
  <h4 class="modal-title" id="addModalLabel">Adicionar Livro</h4>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
</div>
<form
  hx-post="{% url 'bookstore:book_create' %}"
  hx-target="#bookTbody"
  hx-indicator=".htmx-indicator"
  hx-swap="afterbegin"
>
  <div class="modal-body">
    {% csrf_token %}
    {% for field in form %}
      <div class="form-group p-2">
        {{ field.label_tag }}
        {{ field }}
        {{ field.errors }}
        {% if field.help_text %}
          <small class="text-muted">{{ field.help_text|safe }}</small>
        {% endif %}
      </div>
    {% endfor %}
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
    <button type="submit" class="btn btn-primary">Salvar</button>
  </div>
</form>

<script>
  $('form').on('submit', function() {
    $('#addModal').modal('toggle')
  });
</script>
EOF
```

## Detalhes

Vamos editar:

* bookstore/views.py
* bookstore/urls.py
* bookstore/templates/bookstore/book_detail.html
* bookstore/templates/bookstore/includes/detail_modal.html
* bookstore/templates/bookstore/hx/book_result_hx.html
* bookstore/templates/bookstore/book_list.html


Edite `bookstore/views.py`

```python
def book_detail(request, pk):
    template_name = 'bookstore/book_detail.html'
    obj = Book.objects.get(pk=pk)
    context = {'object': obj}
    return render(request, template_name, context)
```

Edite `bookstore/urls.py`

```python
...
path('<int:pk>/', v.book_detail, name='book_detail'),
...
```

```html
cat << EOF > backend/bookstore/templates/bookstore/book_detail.html
<div class="modal-header">
  <h4 class="modal-title" id="detailModalLabel">{{ object.title }}</h4>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
</div>
<div class="modal-body">
  <p>Título
    <span class="float-right">{{ object.title }}</span>
  </p>
  <p>Autor
    <span class="float-right">{{ object.author|default:'---' }}</span>
  </p>
</div>
<div class="modal-footer">
  <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
</div>
EOF
```


```html
cat << EOF > backend/bookstore/templates/bookstore/includes/detail_modal.html
<!-- detailModal -->
<div class="modal fade" id="detailModal" tabindex="-1" role="dialog" aria-labelledby="detailModalLabel">
  <div class="modal-dialog" role="document">
    <div id="detailContent" class="modal-content">
      <!-- O novo conteúdo será inserido aqui. -->
      <div class="modal-header">
        <h4 class="modal-title" id="detailModalLabel">Modal title</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
        <button type="submit" class="btn btn-primary">Salvar</button>
      </div>
    </div>
  </div>
</div>
EOF
```



Edite `backend/bookstore/templates/bookstore/hx/book_result_hx.html`

```html
<!-- book_result_hx.html -->
<tr id="trBook{{ object.pk }}">
  <td>
    <a
      href=""
      data-toggle="modal"
      data-target="#detailModal"
      hx-get="{{ object.get_absolute_url }}"
      hx-target="#detailContent"
      hx-indicator=".htmx-indicator"
      hx-swap="innerHTML"
    >{{ object.title }}</a>
  </td>
  <td>{{ object.author|default:'---' }}</td>
  <td></td>
</tr>
```

Edite `backend/bookstore/templates/bookstore/book_list.html`

```html
...
{% include "./includes/detail_modal.html" %}
...
```


## Editar

Vamos editar:

* bookstore/views.py
* bookstore/urls.py
* bookstore/templates/bookstore/book_list.html
* bookstore/templates/bookstore/includes/update_modal.html
* bookstore/templates/bookstore/hx/book_result_hx.html
* bookstore/templates/bookstore/book_update_form.html



Edite `bookstore/views.py`

```python
def book_update(request, pk):
    template_name = 'bookstore/book_update_form.html'
    instance = Book.objects.get(pk=pk)
    form = BookForm(request.POST or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            book = form.save()
            template_name = 'bookstore/hx/book_result_hx.html'
            context = {'object': book}
            return render(request, template_name, context)

    context = {'form': form, 'object': instance}
    return render(request, template_name, context)

```

Edite `bookstore/urls.py`

```python
...
path('<int:pk>/update/', v.book_update, name='book_update'),
...
```


Edite `backend/bookstore/templates/bookstore/book_list.html`

```html
{% include "./includes/update_modal.html" %}
```

```html
cat << EOF > backend/bookstore/templates/bookstore/includes/update_modal.html
<!-- updateModal -->
<div class="modal fade" id="updateModal" tabindex="-1" role="dialog" aria-labelledby="updateModalLabel">
  <div class="modal-dialog" role="document">
    <div id="updateContent" class="modal-content">
      <!-- O novo conteúdo será inserido aqui. -->
      <div class="modal-header">
        <h4 class="modal-title" id="updateModalLabel">Modal title</h4>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
      </div>
      <div class="modal-body">
        ...
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
        <button type="submit" class="btn btn-primary">Salvar</button>
      </div>
    </div>
  </div>
</div>
EOF
```

Editar `backend/bookstore/templates/bookstore/hx/book_result_hx.html`

```html
<span
  data-toggle="modal"
  data-target="#updateModal"
  hx-get="{% url 'bookstore:book_update' object.pk %}"
  hx-target="#updateContent"
  hx-swap="innerHTML"
>
  <i class="fa fa-edit link span-is-link"></i>
</span>
```

```html
cat << EOF > backend/bookstore/templates/bookstore/book_update_form.html
<div class="modal-header">
  <h4 class="modal-title" id="updateModalLabel">Editar {{ object }}</h4>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
</div>
<form
  hx-post="{% url 'bookstore:book_update' object.pk %}"
  hx-target="#trBook{{ object.pk }}"
  hx-indicator=".htmx-indicator"
  hx-swap="outerHTML"
>
  <div class="modal-body">
    {% csrf_token %}
    {% for field in form %}
      <div class="form-group p-2">
        {{ field.label_tag }}
        {{ field }}
        {{ field.errors }}
        {% if field.help_text %}
          <small class="text-muted">{{ field.help_text|safe }}</small>
        {% endif %}
      </div>
    {% endfor %}
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
    <button type="submit" class="btn btn-primary">Salvar</button>
  </div>
</form>

<script>
  $('form').on('submit', function() {
    $('#updateModal').modal('toggle')
  });
</script>
EOF
```

## Deletar

Vamos editar:

* bookstore/views.py
* bookstore/urls.py
* bookstore/templates/bookstore/book_list.html
* bookstore/templates/bookstore/hx/book_result_hx.html



Edite `bookstore/views.py`

```python
@require_http_methods(['DELETE'])
def book_delete(request, pk):
    template_name = 'bookstore/book_table.html'
    obj = Book.objects.get(pk=pk)
    obj.delete()
    return render(request, template_name)

```


Edite `bookstore/urls.py`

```python
...
path('<int:pk>/delete/', v.book_delete, name='book_delete'),
...
```


Editar `backend/bookstore/templates/bookstore/book_list.html`

```html

{% block js %}
<script>
// Necessário por causa do delete
document.body.addEventListener('htmx:configRequest', (event) => {
  event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
});
</script>
{% endblock js %}

```


Editar `backend/bookstore/templates/bookstore/hx/book_result_hx.html`

Ao lado icone de editar.

```html
...
<span
  hx-delete="{% url 'bookstore:book_delete' object.pk %}"
  hx-confirm="Deseja mesmo deletar?"
  hx-target="closest tr"
  hx-swap="outerHTML swap:500ms"
>
  <i class="fa fa-trash no span-is-link pl-2"></i>
</span>
...
```

## Like e Unlike

Vamos editar:

* bookstore/models.py
* bookstore/admin.py
* bookstore/forms.py
* bookstore/book_list.html
* bookstore/hx/book_result_hx.html
* bookstore/urls.py
* bookstore/views.py

Edite `models.py`

```python
...
like = models.BooleanField(null=True)
```


Edite `admin.py`

```python
...
list_display = ('title', 'author', 'like')
...
```


Edite `forms.py`

```python
...
fields = ('title', 'author')
...
```


Edite `book_list.html`

```html
<th>Gostou?</th>
```


Edite `hx/book_result_hx.html`

```html
<td>
  <span
    hx-post="{% url 'bookstore:book_like' object.pk %}"
    hx-target="#trBook{{ object.pk }}"
    hx-swap="outerHTML"
  >
    {% if object.like %}
      <i class="fa fa-thumbs-up text-primary"></i>
    {% else %}
      <i class="fa fa-thumbs-o-up text-secondary"></i>
    {% endif %}
  </span>
  <span
    class="ml-2"
    hx-post="{% url 'bookstore:book_unlike' object.pk %}"
    hx-target="#trBook{{ object.pk }}"
    hx-swap="outerHTML"
  >
    {% if not object.like %}
      <i class="fa fa-thumbs-down text-danger"></i>
    {% else %}
      <i class="fa fa-thumbs-o-down text-secondary"></i>
    {% endif %}
  </span>
</td>
```


Edite `urls.py`

```python
...
path('<int:pk>/like/', v.book_like, name='book_like'),
path('<int:pk>/unlike/', v.book_unlike, name='book_unlike'),
```


Edite `views.py`

```python
@require_http_methods(['POST'])
def book_like(request, pk):
    template_name = 'bookstore/hx/book_result_hx.html'
    book = Book.objects.get(pk=pk)
    book.like = True
    book.save()
    context = {'object': book}
    return render(request, template_name, context)


@require_http_methods(['POST'])
def book_unlike(request, pk):
    template_name = 'bookstore/hx/book_result_hx.html'
    book = Book.objects.get(pk=pk)
    book.like = False
    book.save()
    context = {'object': book}
    return render(request, template_name, context)
```


## Criar uma nova categoria

Vamos editar:

* settings.py
* urls.py
* apps.py
* models.py
* admin.py
* urls.py
* views.py
* nav.html
* product_list.html
* product_table.html
* includes/add_modal.html
* hx/product_result_hx.html
* hx/category_modal_form_hx.html


Edite `settings.py`

```python
'backend.product',
```


Edite `urls.py`

```python
path('product/', include('backend.product.urls', namespace='product')),
```


Edite `apps.py`

```python
name = 'backend.product'
```


Edite `models.py`

```python
from django.db import models


class Category(models.Model):
    title = models.CharField('título', max_length=100, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField('título', max_length=100, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='categoria',
        related_name='products',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('title',)
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return self.title

```


Edite `admin.py`

```python
from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category')
    search_fields = ('title', 'category__title')

```


Edite `urls.py`

```python
from django.urls import path

from backend.product import views as v

app_name = 'product'


urlpatterns = [
    path('', v.product_list, name='product_list'),
    path('category/<int:pk>/create/', v.category_create, name='category_create'),
]

```


Edite `views.py`

```python
from django.shortcuts import render

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

```


Edite `nav.html`

```html
<li class="nav-item">
  <a class="nav-link" href="{% url 'product:product_list' %}">Produtos</a>
</li>

```


Edite `product_list.html`

```html
<!-- product_list.html -->
{% extends "base.html" %}

{% block content %}
<div>
  <div class="row">
    <div class="col-auto">
      <h1>Lista de Produtos</h1>
    </div>
  </div>
  <table class="table">
    <thead>
      <tr>
        <th>Produto</th>
        <th>Categoria</th>
      </tr>
    </thead>
    <tbody id="productTbody">
      {% include "./product_table.html" %}
    </tbody>
  </table>
</div>

{% include "./includes/add_modal.html" %}

{% endblock content %}

```


Edite `product_table.html`

```html
<!-- product_table.html -->
{% for object in object_list %}
  {% include "./hx/product_result_hx.html" %}
{% endfor %}

```


Edite `hx/product_result_hx.html`

```html
<!-- hx/product_result_hx.html -->
<tr id="trProduct{{ object.pk }}">
  <td>{{ object.title }}</td>
  <td>
    <div class="row">
      <div class="col">
        <select
          id="id_category"
          name="category"
          class="form-control"
        >
          <option value="">-----</option>
          {% for category in categories %}
            <option
              value="{{category.id}}"
              {% if object.category == category %}selected{% endif %}
            >{{ category.title }}</option>
          {% endfor %}
        </select>
      </div>
      <div class="col-auto d-flex align-items-end">
        <span
          data-toggle="modal"
          data-target="#addModal"
          hx-get="{% url 'product:category_create' object.pk %}"
          hx-target="#addContent"
          hx-swap="innerHTML"
        >
          <i class="fa fa-plus-circle fa-2x ok"></i>
        </span>
      </div>
    </div>
  </td>
</tr>
```


Edite `includes/add_modal.html`

```html
<!-- addModal -->
<div class="modal fade" id="addModal" tabindex="-1" role="dialog" aria-labelledby="addModalLabel">
  <div class="modal-dialog" role="document">
    <div id="addContent" class="modal-content">
      <!-- O novo conteúdo será adicionado aqui. -->
    </div>
  </div>
</div>

```


Edite `hx/category_modal_form_hx.html`

```html
<!-- category_modal_form_hx.html -->
<div class="modal-header">
  <h4 id="detailModalLabel" class="modal-title">Adicionar Categoria para {{ object.title }}</h4>
  <button type="button" class="close" data-dismiss="modal" aria-label="Close">
    <span aria-hidden="true">&times;</span></button>
</div>
<form
  hx-post="{% url 'product:category_create' object.pk %}"
  hx-target="#trProduct{{ object.pk }}"
  hx-swap="outerHTML"
>
  {% csrf_token %}
  <div class="modal-body">
    <label>Categoria</label>
    <input id="id_categoria" name="categoria" class="form-control" type="text" />
  </div>
  <div class="modal-footer">
    <button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>
    <button type="submit" class="btn btn-primary">Salvar</button>
  </div>
</form>

<script>
  $('form').on('submit', function() {
    $('#addModal').modal('toggle')
  });
</script>

```


`./manage.py shell_plus`


```python
Category.objects.create(title='bebida')
Category.objects.create(title='lanche')

produtos = [
    ('Água mineral', 'bebida'),
    ('Refrigerante 350ml', 'bebida'),
    ('Batata frita', 'bebida'),
    ('Casquinha', ''),
]

for produto in produtos:
    categoria_titulo = produto[1]
    category = Category.objects.filter(title=categoria_titulo).first()
    if category:
        Product.objects.create(title=produto[0], category=category)
    else:
        Product.objects.create(title=produto[0])

```

## Trocar a categoria

Vamos editar:

* hx/product_result_hx.html
* product_list.html
* urls.py
* views.py


Edite `hx/product_result_hx.html`

```html
<select
  id="id_category"
  name="category"
  class="form-control"
  hx-post="{% url 'product:category_update' object.pk %}"
  hx-swap="none"
>
```


Edite `product_list.html`

```html

{% block js %}
<script>
  // Por causa do editar categoria.
  document.body.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = '{{ csrf_token }}';
  });
</script>
{% endblock js %}

```


Edite `urls.py`

```python
path('<int:product_pk>/category/update/', v.category_update, name='category_update'),  # noqa E501
```


Edite `views.py`

```python
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Category, Product

...

@require_http_methods(['POST'])
def category_update(request, product_pk):
    product = Product.objects.get(pk=product_pk)

    category_pk = request.POST.get('category')
    category = Category.objects.get(pk=category_pk)

    product.category = category
    product.save()
    return HttpResponse('ok')

```

