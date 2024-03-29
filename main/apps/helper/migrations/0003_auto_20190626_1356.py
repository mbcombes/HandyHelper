# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-26 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0002_job_helper'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='job',
            name='category',
        ),
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.ManyToManyField(related_name='jobs', to='helper.Category'),
        ),
    ]
