# Generated by Django 3.1.5 on 2021-04-19 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenge', '0012_auto_20210416_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='two_way',
            field=models.BooleanField(default=False),
        ),
    ]
