# Generated by Django 4.2 on 2023-06-04 08:51

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0012_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accountant',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('gestion.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
