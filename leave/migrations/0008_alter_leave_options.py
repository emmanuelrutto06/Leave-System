# Generated by Django 3.2.19 on 2023-06-16 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0007_auto_20230616_0631'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leave',
            options={'ordering': ['-created'], 'verbose_name': 'Leave', 'verbose_name_plural': 'Leaves'},
        ),
    ]
