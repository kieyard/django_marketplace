# Generated by Django 3.1.7 on 2021-04-29 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_status',
            field=models.BooleanField(default=False),
        ),
    ]