# Generated by Django 3.1.5 on 2021-03-29 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0008_auto_20210329_0759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='language',
            field=models.CharField(choices=[('cpp', 'C++'), ('java', 'Java'), ('py3', 'Python 3'), ('jar', 'Jar')], default='java', max_length=50),
        ),
    ]
