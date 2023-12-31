# Generated by Django 4.2 on 2023-05-21 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0003_alter_city_options_alter_company_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField(default=0.0)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.company')),
                ('trimester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.trimester')),
            ],
        ),
    ]
