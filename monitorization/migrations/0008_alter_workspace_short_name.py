# Generated by Django 4.2.7 on 2024-01-22 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorization', '0007_alter_workspace_name_alter_workspace_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='short_name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
