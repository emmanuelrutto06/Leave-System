# Generated by Django 4.2.3 on 2023-08-09 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0013_leave_default_annual_leave_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='total_leave_days_available',
        ),
    ]
