# Generated by Django 4.2.7 on 2024-05-14 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='status',
            field=models.CharField(blank=True, choices=[('single', 'Single'), ('married', 'Married'), ('widowed', 'Widowed'), ('divorced', 'Divorced'), ('prefer_not_to_say', 'Prefer Not to Say')], max_length=100),
        ),
    ]
