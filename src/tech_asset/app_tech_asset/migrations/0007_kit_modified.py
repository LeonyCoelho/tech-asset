# Generated by Django 5.0.6 on 2024-07-08 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tech_asset', '0006_kit_subsectors_kithistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='kit',
            name='modified',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]