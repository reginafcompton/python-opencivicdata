# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 01:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opencivicdata', '0006_auto_20170220_2057'),
    ]

    operations = [
        migrations.AddField(
            model_name='voteevent',
            name='bill_action',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vote', to='opencivicdata.BillAction'),
        ),
        migrations.AlterField(
            model_name='jurisdiction',
            name='classification',
            field=models.CharField(choices=[('government', 'Government'), ('legislature', 'Legislature'), ('executive', 'Executive'), ('school', 'School System'), ('park', 'Park District'), ('sewer', 'Sewer District'), ('forest', 'Forest Preserve District'), ('transit_authority', 'Transit Authority')], db_index=True, default='government', max_length=50),
        ),
        migrations.AlterField(
            model_name='organization',
            name='classification',
            field=models.CharField(blank=True, choices=[('legislature', 'Legislature'), ('executive', 'Executive'), ('upper', 'Upper Chamber'), ('lower', 'Lower Chamber'), ('party', 'Party'), ('committee', 'Committee'), ('commission', 'Commission'), ('corporation', 'Corporation'), ('agency', 'Agency'), ('department', 'Department')], max_length=100),
        ),
    ]
