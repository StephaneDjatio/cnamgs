# Generated by Django 4.2 on 2023-05-26 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0009_companyappointedmission'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_number',
            field=models.CharField(default='null', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]