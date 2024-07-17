# Generated by Django 5.0.6 on 2024-07-12 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tech_asset', '0011_kithistory_new_sector_kithistory_new_subsector_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kit',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='kithistory',
            name='assets',
        ),
        migrations.AddField(
            model_name='asset',
            name='kit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_tech_asset.kit'),
        ),
    ]