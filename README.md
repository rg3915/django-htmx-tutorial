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
* [Filtrar com dropdowns dependentes](#filtrar-com-dropdowns-dependentes)
* [Adicionar itens](#adicionar-itens)
* [Pagar (editar) vários itens (Bulk Update)](#pagar-editar-vários-itens-bulk-update)
* [Editar um item](#editar-um-item)
* [Deletar um item](#deletar-um-item)
* [client-side-templates](#client-side-templates)


## Passo a passo

## Exemplos

### Filtrar várias tabelas com um clique

![a02_tabela.png](img/a02_tabela.png)

---

### Filtrar com dropdowns dependentes

![a01_combobox.png](img/a01_combobox.png)

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

