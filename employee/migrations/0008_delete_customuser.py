# Generated by Django 4.2.3 on 2023-07-14 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0007_alter_customuser_options_customuser_groups_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
