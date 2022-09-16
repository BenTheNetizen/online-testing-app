# Generated by Django 3.1.7 on 2022-09-16 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_auto_20210823_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_premium',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='payment_status',
            field=models.CharField(choices=[('SUCCESS', 'Success'), ('CANCELLED', 'Cancelled'), ('NONE', 'None')], default='NONE', max_length=9),
        ),
    ]
