# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-06-26 18:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='helper',
            field=models.ManyToManyField(related_name='jobs', to='helper.User'),
        ),
    ]
