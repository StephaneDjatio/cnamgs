# Generated by Django 4.2 on 2023-06-10 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0016_inspect_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspect',
            name='inspection_report',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
