# Generated by Django 2.1.5 on 2023-06-29 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20230629_1243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_superadmin',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
