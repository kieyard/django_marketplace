# Generated by Django 3.1.7 on 2021-05-03 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('is_buyer', models.BooleanField(default=True)),
                ('is_seller', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('stripe_customer_id', models.CharField(max_length=40)),
                ('stripe_seller_id', models.CharField(default='', max_length=40)),
                ('stripe_seller_TOS_accepted', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AddCardSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_holders_fullname', models.CharField(max_length=80)),
                ('card_number', models.CharField(max_length=16)),
                ('exp_month', models.IntegerField()),
                ('exp_year', models.IntegerField()),
                ('cvc', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='StripeConnectSetup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('DOB', models.DateField()),
                ('phone', models.CharField(max_length=13)),
                ('address_line_1', models.CharField(max_length=100)),
                ('address_line_2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=3)),
                ('postal_code', models.CharField(max_length=7)),
                ('identity_document_front', models.ImageField(blank=True, upload_to='images')),
                ('identity_document_back', models.ImageField(blank=True, upload_to='images')),
                ('additional_ID', models.ImageField(blank=True, upload_to='images')),
                ('payout_sort_code', models.CharField(max_length=6)),
                ('payout_account_number', models.CharField(max_length=8)),
                ('accept_TOS', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, null=True)),
                ('last_name', models.CharField(max_length=40, null=True)),
                ('address_line_1', models.CharField(max_length=100, null=True)),
                ('address_line_2', models.CharField(max_length=100, null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('postal_code', models.CharField(max_length=7, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(max_length=40, null=True)),
                ('last_4', models.CharField(max_length=4, null=True)),
                ('brand', models.CharField(max_length=40)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
