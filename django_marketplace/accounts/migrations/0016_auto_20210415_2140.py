# Generated by Django 3.1.7 on 2021-04-15 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20210415_2123'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AddDeliveryAddress',
            new_name='DeliveryAddress',
        ),
    ]
