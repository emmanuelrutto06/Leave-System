# Generated by Django 4.2.3 on 2023-08-29 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0019_holiday'),
    ]

    operations = [
        migrations.AddField(
            model_name='holiday',
            name='holiday_name',
            field=models.CharField(default='To be Updated', max_length=100),
        ),
        migrations.AlterField(
            model_name='holiday',
            name='holiday_type',
            field=models.CharField(choices=[('public', 'Public Holiday'), ('company', 'Company Holiday')], max_length=10),
        ),
    ]
