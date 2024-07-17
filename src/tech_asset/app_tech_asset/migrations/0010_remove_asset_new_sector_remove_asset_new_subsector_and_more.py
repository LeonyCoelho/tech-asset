# Generated by Django 5.0.6 on 2024-07-11 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tech_asset', '0009_asset_new_sector_asset_new_subsector_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='new_sector',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='new_subsector',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='previous_sector',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='previous_subsector',
        ),
        migrations.AddField(
            model_name='assethistory',
            name='new_sector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assethistory',
            name='new_subsector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assethistory',
            name='previous_sector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assethistory',
            name='previous_subsector',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='assethistory',
            name='subsector',
            field=models.CharField(max_length=50, null=True),
        ),
    ]