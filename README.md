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

<img src="img/a02_tabela.png" alt="" width="200px">


* [Filtrar com dropdowns dependentes](#filtrar-com-dropdowns-dependentes)

<img src="img/a01_combobox.png" alt="" width="200px">


* [Adicionar itens](#adicionar-itens)

<img src="img/01_expense_add.png" alt="" width="200px">


* [Pagar (editar) vários itens (Bulk Update)](#pagar-editar-vários-itens-bulk-update)

<img src="img/02_expense_bulk_update.png" alt="" width="200px">


* [Editar um item](#editar-um-item)

<img src="img/03_expense_update.png" alt="" width="200px">


* [Deletar um item](#deletar-um-item)

<img src="img/04_expense_delete.png" alt="" width="200px">


* [client-side-templates](#client-side-templates)




## Passo a passo

Em `base.html` escreva

```html
<!-- HTMX -->
<script src="https://unpkg.com/htmx.org@1.5.0"></script>
<script src="https://unpkg.com/htmx.org@1.5.0/dist/ext/client-side-templates.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mustache@4.2.0/mustache.min.js"></script>
```

Em `nav.html` escreva

```html
<li class="nav-item">
  <a class="nav-link" href="{ url 'state:state_list' %}">Estados</a>
</li>
<li class="nav-item">
  <a class="nav-link" href="{ url 'expense:expense_list' %}">Despesas</a>
</li>
<li class="nav-item">
  <a class="nav-link" href="{ url 'expense:expense_client' %}">Despesas (Client side)</a>
</li>
```



## Exemplos

### Filtrar várias tabelas com um clique

![a02_tabela.png](img/a02_tabela.png)

Considere a app `state`.

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
mkdir -p state/templates/state
```


Escreva o template `state/templates/state/state_list.html`

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
    template_name = 'state/state_result.html'
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

Escreva o template `state/templates/state/state_result.html`

```html
<!-- state/templates/state/state_result.html -->
{% for uf in ufs %}
  <tr>
    <td>{{ uf.1 }}</td>
  </tr>
{% endfor %}
```

---

### Filtrar com dropdowns dependentes

![a01_combobox.png](img/a01_combobox.png)

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
    template_name = 'state/uf_list.html'
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

Edite `state/uf_list.html`

```html
<!-- state/uf_list.html -->

```

---

### 

![expense_base.png](img/expense_base.png)

---

### Adicionar itens

![01_expense_add.png](img/01_expense_add.png)

---

### Pagar (editar) vários itens (Bulk Update)

![02_expense_bulk_update.png](img/02_expense_bulk_update.png)

---

### Editar um item

![03_expense_update.png](img/03_expense_update.png)

---

### Deletar um item

![04_expense_delete.png](img/04_expense_delete.png)

---

### client-side-templates

https://htmx.org/extensions/client-side-templates/


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

