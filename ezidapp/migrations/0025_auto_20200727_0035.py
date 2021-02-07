# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-27 00:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ezidapp', '0024_downloadqueue_filesize'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoulderType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shoulder_type', models.CharField(editable=False, max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='shoulder',
            name='active',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='shoulder',
            name='date',
            field=models.DateField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='shoulder',
            name='isSupershoulder',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='shoulder',
            name='manager',
            field=models.CharField(blank=True, editable=False, max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='shoulder',
            name='prefix_shares_datacenter',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='shoulder',
            name='redirect',
            field=models.URLField(blank=True, editable=False, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shoulder',
            name='shoulder_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ezidapp.ShoulderType'),
        ),
    ]
