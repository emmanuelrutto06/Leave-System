# Generated by Django 3.2.19 on 2023-06-16 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0006_alter_leave_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='remaining_leave_days',
            new_name='leave_days_remaining',
        ),
        migrations.RenameField(
            model_name='leave',
            old_name='taken_leave_days',
            new_name='leave_days_taken',
        ),
    ]
