# Generated by Django 4.2.7 on 2024-06-05 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='leavetype',
            field=models.CharField(choices=[('annual', 'annual'), ('sick', 'Sick Leave'), ('casual', 'Casual Leave'), ('emergency', 'Emergency Leave'), ('study', 'Study Leave'), ('maternity', 'Maternity Leave'), ('bereavement', 'Bereavement Leave'), ('quarantine', 'Self Quarantine'), ('compensatory', 'Compensatory Leave'), ('sabbatical', 'Sabbatical Leave')], default='SICK', max_length=25, null=True),
        ),
    ]
