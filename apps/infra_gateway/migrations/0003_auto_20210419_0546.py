# Generated by Django 3.1.5 on 2021-04-19 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infra_gateway', '0002_auto_20210416_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infraeventpush',
            name='status_code',
            field=models.PositiveSmallIntegerField(choices=[(100, 100), (102, 102), (402, 402), (404, 404), (500, 500), (502, 502), (504, 504), (506, 506), (508, 508)], default=200),
        ),
    ]
