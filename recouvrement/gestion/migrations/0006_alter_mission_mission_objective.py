# Generated by Django 4.2 on 2023-05-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0005_inspectionquestion_mission_mission_order_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='mission_objective',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
