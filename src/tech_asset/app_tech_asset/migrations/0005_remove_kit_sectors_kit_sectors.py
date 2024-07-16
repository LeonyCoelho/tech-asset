# Generated by Django 5.0.6 on 2024-06-21 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tech_asset', '0004_kit_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kit',
            name='sectors',
        ),
        migrations.AddField(
            model_name='kit',
            name='sectors',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_tech_asset.sector'),
        ),
    ]
