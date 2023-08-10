# Generated by Django 4.2.3 on 2023-08-09 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0012_remove_leave_default_annual_leave_days_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leave',
            name='default_annual_leave_days',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AddField(
            model_name='leave',
            name='leave_days_remaining',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leave',
            name='leave_days_taken',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leave',
            name='total_leave_days_available',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
