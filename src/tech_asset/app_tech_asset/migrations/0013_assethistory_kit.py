# Generated by Django 5.0.6 on 2024-07-17 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tech_asset', '0012_remove_kit_assets_remove_kithistory_assets_asset_kit'),
    ]

    operations = [
        migrations.AddField(
            model_name='assethistory',
            name='kit',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
