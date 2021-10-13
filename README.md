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

## Passo a passo

https://github.com/rg3915/django-htmx-tutorial#passo-a-passo