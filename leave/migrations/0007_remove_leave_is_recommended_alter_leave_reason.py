# Generated by Django 4.2.3 on 2023-07-27 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0006_leave_is_recommended_alter_leave_reason'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave',
            name='is_recommended',
        ),
        migrations.AlterField(
            model_name='leave',
            name='reason',
            field=models.CharField(blank=True, help_text='add additional information for leave', max_length=255, null=True, verbose_name='Reason for Leave'),
        ),
    ]
