# Generated by Django 4.2 on 2023-06-10 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0015_manager_managerprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspect',
            name='company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion.company'),
        ),
    ]
