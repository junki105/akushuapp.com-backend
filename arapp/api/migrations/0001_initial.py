# Generated by Django 3.1.7 on 2022-04-07 06:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('address1', models.CharField(blank=True, max_length=50, null=True)),
                ('address2', models.CharField(blank=True, max_length=50, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('email_verified_hash', models.CharField(blank=True, max_length=50, null=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
