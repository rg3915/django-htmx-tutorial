# Generated by Django 3.2.5 on 2021-12-07 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='like',
            field=models.BooleanField(null=True),
        ),
    ]
