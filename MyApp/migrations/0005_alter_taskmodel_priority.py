# Generated by Django 5.1.7 on 2025-03-11 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0004_alter_taskmodel_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskmodel',
            name='priority',
            field=models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High')], max_length=10, null=True),
        ),
    ]
