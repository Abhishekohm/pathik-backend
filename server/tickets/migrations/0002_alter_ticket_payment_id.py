# Generated by Django 4.1.1 on 2022-12-20 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='payment_id',
            field=models.CharField(max_length=100),
        ),
    ]
