# Generated by Django 4.2 on 2023-05-22 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0007_agentappointedmission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='mission_date',
            field=models.DateField(),
        ),
    ]