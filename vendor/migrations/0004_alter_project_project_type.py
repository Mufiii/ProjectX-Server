# Generated by Django 4.2.7 on 2024-01-02 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_alter_project_project_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.CharField(choices=[('One-time project', 'One-time project'), ('Ongoing project', 'Ongoing Project')], max_length=150),
        ),
    ]
