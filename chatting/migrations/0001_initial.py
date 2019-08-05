# Generated by Django 2.2 on 2019-06-22 07:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=15, verbose_name='user')),
                ('date', models.DateTimeField(default=datetime.datetime(2019, 6, 22, 7, 34, 45, 301657, tzinfo=utc), verbose_name='message time')),
                ('message', models.TextField(verbose_name='message')),
                ('room', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.TextField(verbose_name='name')),
            ],
        ),
    ]