# Generated by Django 3.1.7 on 2021-05-11 20:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0002_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(default='', max_length=1)),
                ('question_number', models.IntegerField(default=0)),
                ('section', models.CharField(default='', max_length=30)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
