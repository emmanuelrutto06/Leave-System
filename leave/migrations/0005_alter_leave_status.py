# Generated by Django 4.2.3 on 2023-07-18 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0004_alter_leave_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]
